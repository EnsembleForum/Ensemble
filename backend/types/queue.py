from typing import TypedDict
from .identifiers import QueueId, PostId


class IQueueId(TypedDict):
    """
    Identifier of a queue

    * `queue_id`: `QueueId`
    """
    queue_id: QueueId


class IQueueBasicInfo(TypedDict):
    """
    Basic info about a queue

    * `queue_name`: `str`
    * `queue_id`: `QueueId`
    * `view_only`: `bool`
    """
    queue_id: QueueId
    queue_name: str
    view_only: bool


class IQueueFullInfo(TypedDict):
    """
    Full info about a queue

    * `queue_id`: `QueueId`
    * `queue_name`: `str`
    * `posts`: `list[PostId]`
    * `view_only`: `bool`
    """
    queue_id: QueueId
    queue_name: str
    posts: list[PostId]
    view_only: bool


class IQueueList(TypedDict):
    """
    List of basic info about queues
    """
    queues: list[IQueueBasicInfo]
