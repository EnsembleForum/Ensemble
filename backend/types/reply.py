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
    * `user_reacted`: `bool`
    * `deleted`: `bool`
    """
    reply_id: ReplyId
    author: UserId
    thanks: int
    text: str
    timestamp: int
    user_reacted: bool
    deleted: bool
