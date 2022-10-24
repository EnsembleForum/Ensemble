"""
# Tests / Integration / Request / Taskboard

Helper functions for requesting queue-related code
"""
from typing import cast
from backend.types.queue import IQueueId, IQueueFullInfo, IQueueList
from backend.types.identifiers import QueueId
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get


URL = f"{URL}/taskboard"


def queue_list(token: JWT, queue_id: QueueId) -> IQueueList:
    """
    Get a list of queues

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IQueueInfoList`: List of basic info of queues
    """
    return cast(
        IQueueList,
        get(token,
            f"{URL}/queue_list",
            {}
            ),
    )


def queue_create(
    token: JWT, queue_name: str
) -> IQueueId:
    """
    Create a queue
    """
    return cast(
        IQueueId,
        post(token,
             f"{URL}/queue_list/create",
             {
                 "queue_name": queue_name,
             },
             ),
    )


def post_list(token: JWT, queue_id: QueueId) -> IQueueFullInfo:
    """
    Get a detailed info of a queue

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IQueueInfo`: List of basic info of queues
    """
    return cast(
        IQueueFullInfo,
        get(token,
            f"{URL}/queue/post_list",
            {
                "queue_id": queue_id,
            }
            ),
    )
