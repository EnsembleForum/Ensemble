from typing import TypedDict
from .identifiers import CommentId, ReplyId, UserId


class ICommentId(TypedDict):
    """
    Identifier of a comment

    * `comment_id`: `CommentId`
    """

    comment_id: CommentId


class ICommentFullInfo(TypedDict):
    """
    Full info about a comment

    * `author`: `UserId`
    * `text`: `str`
    * `thanks`: `int`
    * `replies`: `list[ReplyId]`
    * `timestamp`: `int`
    """
    author: UserId
    thanks: int
    replies: list[ReplyId]
    text: str
    timestamp: int
    user_reacted: bool
