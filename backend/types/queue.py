from typing import TypedDict
from .identifiers import QueueId, PostId


class IQueueId(TypedDict):
    """
    Identifier of a queue

    * `post_id`: `PostId`
    """
    queue_id: QueueId


class IQueueBasicInfo(TypedDict):
    """
    Basic info about a queue

    * `queue_name`: `str`
    * `post_id`: `PostId`
    """
    queue_id: QueueId
    queue_name: str


class IQueueFullInfo(TypedDict):
    """
    Full info about a queue

    * `post_id`: `PostId`
    * `queue_name`: `str`
    * `posts`: `list[PostId]`
    """
    queue_id: QueueId
    queue_name: str
    posts: list[PostId]


class IQueueList(TypedDict):
    """
    List of basic info about queues
    """
    queues: list[IQueueBasicInfo]
