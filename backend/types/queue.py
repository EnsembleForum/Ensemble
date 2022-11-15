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

    * `queue_name` (`str`): name of queue
    * `queue_id` (`QueueId`): ID of queue
    * `view_only` (`bool`): whether queue is view only (posts can't be moved
      to/from it)
    * `following` (`bool`): whether the user is following it
    """
    queue_id: QueueId
    queue_name: str
    view_only: bool
    following: bool


class IQueueFullInfo(TypedDict):
    """
    Full info about a queue

    * `queue_name` (`str`): name of queue
    * `queue_id` (`QueueId`): ID of queue
    * `view_only` (`bool`): whether queue is view only (posts can't be moved
      to/from it)
    * `following` (`bool`): whether the user is following it
    * `posts` (`list[int]`): list of post IDs in the queue
    """
    queue_id: QueueId
    queue_name: str
    view_only: bool
    following: bool
    posts: list[PostId]


class IQueueList(TypedDict):
    """
    List of basic info about queues

    * `queues`: List of dicts containing:
            * `queue_name` (`str`): name of queue
            * `queue_id` (`QueueId`): ID of queue
            * `view_only` (`bool`): whether queue is view only (posts can't be
              moved to/from it)
            * `following` (`bool`): whether the user is following it
            * `posts` (`list[int]`): list of post IDs in the queue
    """
    queues: list[IQueueBasicInfo]
