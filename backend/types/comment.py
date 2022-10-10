from typing import TypedDict
from .identifiers import CommentId, ReplyId
from .post import IReacts


class ICommentId(TypedDict):
    """
    Identifier of a comment
    """

    comment_id: CommentId


class ICommentFullInfo(TypedDict):
    author: str
    reacts: IReacts
    replies: list[ReplyId]
    text: str
    timestamp: int
