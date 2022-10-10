"""
# Backend / Routes / Browse / Reply View

Reply View routes
"""
from flask import Blueprint, request
from typing import cast
from backend.models.reply import Reply
from backend.models.token import Token
from backend.types.auth import JWT
from backend.types.identifiers import ReplyId
from backend.types.reply import IReplyFullInfo

reply_view = Blueprint("reply_view", "reply_view")


@reply_view.get("")
def get_reply() -> IReplyFullInfo:
    """
    Get the detailed info of a reply

    ## Body:
    * `reply_id` (`ReplyId`): identifier of the reply
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IReplyFullInfo`: Dictionary containing full info a reply
    """
    reply_id: ReplyId = cast(ReplyId, request.args["reply_id"])
    Token.fromJWT(cast(JWT, request.args["token"]))
    reply = Reply(reply_id)
    return {
        "author": f"{reply.author.name_first} {reply.author.name_last}",
        "reacts": reply.reacts,
        "text": reply.text,
        "timestamp": reply.timestamp,
    }
