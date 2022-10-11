from typing import TypedDict
from .identifiers import CommentId, ReplyId, UserId
from .post import IReacts


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
    * `reacts`: `IReacts`
    * `replies`: `list[ReplyId]`
    * `timestamp`: `int`
    """
    author: UserId
    reacts: IReacts
    replies: list[ReplyId]
    text: str
    timestamp: int
