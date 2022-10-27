"""
# Tests / Integration / Request / Taskboard

Helper functions for requesting queue-related code
"""
from typing import cast
from backend.types.queue import IQueueId, IQueueFullInfo, IQueueList
from backend.types.identifiers import QueueId
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, delete


URL = f"{URL}/taskboard"


def queue_list(token: JWT) -> IQueueList:
    """
    Get a list of queues

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IQueueList`: List of basic info of queues,
       hence queue: list[IQueueBasicInfo]
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
    Creates a queue and returns the queue name
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

    ## Header:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IQueueInfo`: List of basic info of queues
    """
    return cast(
        IQueueFullInfo,
        get(
            token,
            f"{URL}/queue/post_list",
            {
                "queue_id": queue_id,
            }
            ),
    )


def queue_delete(token: JWT, queue_id: QueueId):
    """
    Get a list of queues

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IQueueList`: List of basic info of queues,
       hence queue: list[IQueueBasicInfo]
    """
    IQueueList,
    delete(
        token,
        f"{URL}/queue_list/delete",
        {
            "queue_id": queue_id,
        }
    )
