from typing import TypedDict
from .identifiers import ReplyId, UserId
from .post import IReacts


class IReplyId(TypedDict):
    """
    Identifier of a reply

    * `reply_id`: `ReplyId`
    """

    reply_id: ReplyId


class IReplyFullInfo(TypedDict):
    """
    Full info about a reply

    * `author`: `UserId`
    * `text`: `str`
    * `reacts`: `IReacts`
    * `timestamp`: `int`
    """
    author: UserId
    reacts: IReacts
    text: str
    timestamp: int
