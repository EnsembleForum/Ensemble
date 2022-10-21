from typing import TypedDict
from .identifiers import ReplyId, UserId


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
    * `thanks`: `int`
    * `timestamp`: `int`
    """
    author: UserId
    thanks: int
    text: str
    timestamp: int
