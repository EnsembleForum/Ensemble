from typing import TypedDict
from .identifiers import ReplyId
from .post import IReacts


class IReplyId(TypedDict):
    """
    Identifier of a reply
    """

    reply_id: ReplyId


class IReplyFullInfo(TypedDict):
    author: str
    reacts: IReacts
    text: str
    timestamp: int
