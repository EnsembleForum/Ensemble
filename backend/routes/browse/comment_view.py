"""
# Backend / Routes / Browse / Comment View

Comment View routes
"""
import json
from flask import Blueprint, request
from typing import cast
from backend.models.reply import Reply
from backend.models.comment import Comment
from backend.types.identifiers import ReplyId, UserId, CommentId
from backend.types.comment import ICommentFullInfo
from backend.types.reply import IReplyId

comment_view = Blueprint("comment_view", "comment_view")


@comment_view.get("")
def get_comment() -> ICommentFullInfo:
    """
    Get the detailed info of a comment

    ## Body:
    * `comment_id` (`CommentId`): identifier of the comment

    ## Returns:
    * `ICommentFullInfo`: Dictionary containing full info a comment
    """
    comment_id: CommentId = cast(CommentId, request.args["comment_id"])
    comment = Comment(comment_id)
    return {
        # TODO "author": f"{post.author.name_first} {post.author.name_last}",
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
    * `user_id` (`UserId`): identifier of the author of the reply

    ## Returns:
    * `IReplyId`: identifier of the reply
    """
    data = json.loads(request.data)
    author: UserId = data["user_id"]
    text: str = data["text"]
    comment_id: CommentId = data["comment_id"]

    reply_id: ReplyId = Reply.create(author, comment_id, text).id

    return {"reply_id": reply_id}
