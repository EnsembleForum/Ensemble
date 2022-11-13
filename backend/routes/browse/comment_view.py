"""
# Backend / Routes / Browse / Comment View

Comment View routes
"""
import json
from flask import Blueprint, request
from backend.models.notifications import (
    NotificationCommented,
    NotificationAccepted,
    NotificationUnaccepted,
    NotificationReacted,
)
from backend.models.permissions import Permission
from backend.models.reply import Reply
from backend.models.comment import Comment
from backend.models.user import User
from backend.types.identifiers import CommentId
from backend.types.comment import ICommentFullInfo, ICommentAccepted
from backend.types.react import IUserReacted
from backend.types.reply import IReplyId
from backend.util.tokens import uses_token
from backend.util import http_errors

comment_view = Blueprint("comment_view", "comment_view")


@comment_view.get("")
@uses_token
def get_comment(user: User, *_) -> ICommentFullInfo:
    user.permissions.assert_can(Permission.PostView)
    comment = Comment(CommentId(request.args["comment_id"]))
    return comment.full_info(user)


@comment_view.post("/reply")
@uses_token
def reply(user: User, *_) -> IReplyId:
    user.permissions.assert_can(Permission.PostComment)
    data = json.loads(request.data)
    text: str = data["text"]
    comment = Comment(data["comment_id"])

    reply = Reply.create(user, comment, text)

    if comment.author != user:
        NotificationCommented.create(
            comment.author,
            user,
            reply,
        )
    if (
        comment.parent.author != user
        and comment.author != comment.parent.author
    ):
        NotificationCommented.create(
            comment.parent.author,
            user,
            reply,
        )

    return {"reply_id": reply.id}


@comment_view.put("/react")
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


@comment_view.put("/accept")
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


@comment_view.put("/edit")
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

    comment.text = new_text
    return {}
