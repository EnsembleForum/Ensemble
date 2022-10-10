"""
# Backend / Routes / Browse / Comment View

Comment View routes
"""
import json
from flask import Blueprint, request
from typing import cast
from backend.models.reply import Reply
from backend.models.comment import Comment
from backend.models.token import Token
from backend.types.auth import JWT
from backend.types.identifiers import ReplyId, CommentId
from backend.types.comment import ICommentFullInfo
from backend.types.reply import IReplyId

comment_view = Blueprint("comment_view", "comment_view")


@comment_view.get("")
def get_comment() -> ICommentFullInfo:
    """
    Get the detailed info of a comment

    ## Body:
    * `comment_id` (`CommentId`): identifier of the comment
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `ICommentFullInfo`: Dictionary containing full info a comment
    """
    comment_id: CommentId = cast(CommentId, request.args["comment_id"])
    Token.fromJWT(cast(JWT, request.args["token"]))
    comment = Comment(comment_id)
    return {
        "author": f"{comment.author.name_first} {comment.author.name_last}",
        "reacts": comment.reacts,
        "text": comment.text,
        "replies": [r.id for r in comment.replies],
        "timestamp": comment.timestamp,
    }


@comment_view.post("/reply")
def reply() -> IReplyId:
    """
    Creates a new reply

    ## Body:
    * `text` (`str`): text of the comment
    * `comment_id` (`CommentId`): identifier of the comment to reply to
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IReplyId`: identifier of the reply
    """
    data = json.loads(request.data)
    token: Token = Token.fromJWT(data["token"])
    text: str = data["text"]
    comment_id: CommentId = data["comment_id"]

    reply_id: ReplyId = Reply.create(token.user, comment_id, text).id

    return {"reply_id": reply_id}
