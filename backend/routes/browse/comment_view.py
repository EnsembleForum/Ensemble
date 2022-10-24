"""
# Backend / Routes / Browse / Comment View

Comment View routes
"""
import json
from flask import Blueprint, request
from backend.models.reply import Reply
from backend.models.comment import Comment
from backend.models.user import User
from backend.types.identifiers import CommentId
from backend.types.comment import ICommentFullInfo
from backend.types.reply import IReplyId
from backend.util.tokens import uses_token

comment_view = Blueprint("comment_view", "comment_view")


@comment_view.get("")
@uses_token
def get_comment(*_) -> ICommentFullInfo:
    """
    Get the detailed info of a comment

    ## Body:
    * `comment_id` (`CommentId`): identifier of the comment
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `ICommentFullInfo`: Dictionary containing full info a comment
    """
    comment = Comment(CommentId(request.args["comment_id"]))
    return comment.full_info


@comment_view.post("/reply")
@uses_token
def reply(user: User, *_) -> IReplyId:
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
    text: str = data["text"]
    comment = Comment(data["comment_id"])

    reply_id = Reply.create(user, comment, text).id

    return {"reply_id": reply_id}
