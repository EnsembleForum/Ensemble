"""
# Backend / Routes / Browse / Reply View

Reply View routes
"""
import json
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.models.user import User
from backend.models.reply import Reply
from backend.types.identifiers import ReplyId
from backend.types.reply import IReplyFullInfo
from backend.types.react import IUserReacted
from backend.util.tokens import uses_token

reply_view = Blueprint("reply_view", "reply_view")


@reply_view.get("")
@uses_token
def get_reply(user: User, *_) -> IReplyFullInfo:
    user.permissions.assert_can(Permission.PostView)
    reply_id = ReplyId(request.args["reply_id"])
    reply = Reply(reply_id)
    return reply.full_info(user)


@reply_view.put("/react")
@uses_token
def react(user: User, *_) -> IUserReacted:
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    reply = Reply(data["reply_id"])
    reply.react(user)

    return {"user_reacted": reply.has_reacted(user)}
