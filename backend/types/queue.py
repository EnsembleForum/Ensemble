from typing import TypedDict
from .identifiers import QueueId, PostId


class IQueueId(TypedDict):
    """
    Identifier of a post

    * `post_id`: `PostId`
    """
    queue_id: QueueId


class IQueueFullInfo(TypedDict):
    """
    Full info about a post

    * `queue_name`: `str`
    * `posts`: `list[PostId]`

    """
    queue_name: str
    posts: list[PostId]


class IQueueFullInfoList(TypedDict):
    """
    List of basic info about queues
    """

    posts: list[IQueueFullInfo]
