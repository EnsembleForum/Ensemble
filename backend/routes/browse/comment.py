"""
# Backend / Routes / Browse / Comment View

Comment View routes
"""
import json
from flask import Blueprint, request
from backend.models import Permission, Post, Comment, User
from backend.models.notifications import (
    NotificationCommented,
    NotificationAccepted,
    NotificationUnaccepted,
    NotificationReacted,
    NotificationDeleted
)
from backend.types.identifiers import CommentId
from backend.types.comment import (
    ICommentFullInfo,
    ICommentAccepted,
    ICommentId,
)
from backend.types.react import IUserReacted
from backend.util.tokens import uses_token
from backend.util import http_errors

comment = Blueprint("comment", "comment")


@comment.get("/view")
@uses_token
def view(user: User, *_) -> ICommentFullInfo:
    user.permissions.assert_can(Permission.PostView)
    comment = Comment(CommentId(request.args["comment_id"]))
    return comment.full_info(user)


@comment.post("/create")
@uses_token
def create(user: User, *_) -> ICommentId:
    user.permissions.assert_can(Permission.PostComment)
    data = json.loads(request.data)
    text: str = data["text"]
    post = Post(data["post_id"])

    comment = Comment.create(user, post, text)

    if post.author != user:
        NotificationCommented.create(
            post.author,
            user,
            comment,
        )

    return {"comment_id": comment.id}


@comment.put("/edit")
@uses_token
def edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.PostCreate)
    data = json.loads(request.data)
    comment_id: CommentId = data["comment_id"]
    new_text: str = data["text"]

    comment = Comment(comment_id)

    if user != comment.author:
        raise http_errors.Forbidden(
            "Attempting to edit another user's comment")

    if comment.deleted:
        raise http_errors.BadRequest("Cannot edit a deleted comment")

    comment.text = new_text
    return {}


@comment.delete("/delete")
@uses_token
def delete(user: User, *_) -> dict:
    comment = Comment(CommentId(request.args["comment_id"]))

    if user != comment.author:
        user.permissions.assert_can(Permission.DeletePosts)
        NotificationDeleted.create(
            comment.author,
            comment,
        )

    comment.delete()
    return {}


@comment.put("/react")
@uses_token
def react(user: User, *_) -> IUserReacted:
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    comment = Comment(data["comment_id"])
    comment.react(user)

    if user != comment.author:
        NotificationReacted.create(
            comment.author,
            comment,
        )

    return {"user_reacted": comment.has_reacted(user)}


@comment.put("/accept")
@uses_token
def accept(user: User, *_) -> ICommentAccepted:
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    comment = Comment(data["comment_id"])

    comment.accepted_toggle(user)

    if comment.accepted:
        # Give notification to comment author if they didn't accept it
        # themselves
        if comment.author != user:
            NotificationAccepted.create(
                comment.author,
                user,
                comment,
            )
        # Give notification to post author if they didn't write comment and
        # if they didn't accept it themselves
        if (
            comment.parent.author != user
            and comment.parent.author != comment.author
        ):
            NotificationAccepted.create(
                comment.parent.author,
                user,
                comment,
            )
    else:
        # Comment unaccepted
        # Notify author unless they did it themselves
        if comment.author != user:
            NotificationUnaccepted.create(
                comment.author,
                user,
                comment,
            )
    return {"accepted": comment.accepted}
