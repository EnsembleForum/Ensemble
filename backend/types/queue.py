from typing import TypedDict
from .identifiers import QueueId






class IQueueId(TypedDict):
    """
    Identifier of a post

    * `post_id`: `PostId`
    """
    queue_id: Queue_id

