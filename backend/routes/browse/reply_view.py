"""
# Backend / Routes / Browse / Reply View

Reply View routes
"""
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.models.user import User
from backend.models.reply import Reply
from backend.types.identifiers import ReplyId
from backend.types.reply import IReplyFullInfo
from backend.util.tokens import uses_token

reply_view = Blueprint("reply_view", "reply_view")


@reply_view.get("")
@uses_token
def get_reply(user: User, *_) -> IReplyFullInfo:
    user.permissions.assert_can(Permission.PostView)
    reply_id = ReplyId(request.args["reply_id"])
    reply = Reply(reply_id)
    return reply.full_info
