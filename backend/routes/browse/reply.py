"""
# Backend / Routes / Browse / Reply View

Reply View routes
"""
import json
from flask import Blueprint, request
from backend.models.notifications import (
    NotificationReacted,
    NotificationDeleted,
    NotificationCommented,
)
from backend.models import User, Comment, Reply, Permission
from backend.types.identifiers import ReplyId
from backend.types.reply import IReplyFullInfo, IReplyId
from backend.types.react import IUserReacted
from backend.util.tokens import uses_token
from backend.util import http_errors

reply = Blueprint("reply", "reply")


@reply.get("/view")
@uses_token
def view(user: User, *_) -> IReplyFullInfo:
    user.permissions.assert_can(Permission.PostView)
    reply_id = ReplyId(request.args["reply_id"])
    reply = Reply(reply_id)
    return reply.full_info(user)


@reply.post("/create")
@uses_token
def create(user: User, *_) -> IReplyId:
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


@reply.put("/edit")
@uses_token
def edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.PostCreate)
    data = json.loads(request.data)
    reply_id: ReplyId = data["reply_id"]
    new_text: str = data["text"]

    reply = Reply(reply_id)

    if user != reply.author:
        raise http_errors.Forbidden(
            "Attempting to edit another user's comment")

    if reply.deleted:
        raise http_errors.BadRequest("Cannot edit a deleted reply")

    reply.text = new_text
    return {}


@reply.delete("/delete")
@uses_token
def delete(user: User, *_) -> dict:
    reply = Reply(ReplyId(request.args["reply_id"]))

    if user != reply.author:
        user.permissions.assert_can(Permission.DeletePosts)
        NotificationDeleted.create(
            reply.author,
            reply,
        )

    reply.delete()
    return {}


@reply.put("/react")
@uses_token
def react(user: User, *_) -> IUserReacted:
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    reply = Reply(data["reply_id"])
    reply.react(user)

    if user != reply.author and reply.has_reacted(user):
        NotificationReacted.create(
            reply.author,
            reply,
        )

    return {"user_reacted": reply.has_reacted(user)}
