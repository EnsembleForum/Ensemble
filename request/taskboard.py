"""
# Tests / Integration / Request / Taskboard

Helper functions for requesting queue-related code
"""
from typing import cast
from backend.types.queue import IQueueId, IQueueFullInfo, IQueueList
from backend.types.identifiers import QueueId
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, delete, put


URL = f"{URL}/taskboard"


def queue_list(token: JWT) -> IQueueList:
    """
    ## GET `/taskboard/queue_list`

    Get a list of queues

    ## Header
    * `token` (`JWT`): JWT of the user

    ## Returns
    Object containing:
    * `queues`: list of objects containing:
            * `queue_name` (`str`): the name of the queue
            * `queue_id` (`int`): ID of the queue
    """
    return cast(
        IQueueList,
        get(
            token,
            f"{URL}/queue_list",
            {}
        ),
    )


def queue_create(token: JWT, queue_name: str) -> IQueueId:
    """
    ## POST `/taskboard/queue_list/create`

    Creates a new queue

    ## Header
    * `token` (`JWT`): JWT of the user

    ## Body:
    * `queue_name` (`str`): Name to use for the new queue

    ## Returns
    Object containing:
    * `queue_id` (`int`): ID of the new queue
    """
    return cast(
        IQueueId,
        post(
            token,
            f"{URL}/queue_list/create",
            {
                "queue_name": queue_name,
            },
        ),
    )


def post_list(token: JWT, queue_id: QueueId) -> IQueueFullInfo:
    """
    ## GET `/taskboard/queue/post_list`

    Get a detailed info of a queue

    ## Header
    * `token` (`JWT`): JWT of the user

    ## Params
    * `queue_id` (`int`): ID of the queue to get info on

    ## Returns
    * `queue_id` (`int`): ID of the queue
    * `queue_name` (`str`): name of the queue
    * `posts`: (`list[int]`): list of post IDs in this queue
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
    ## DELETE `/taskboard/queue_list/delete`

    Delete a queue

    ## Header
    * `token` (`JWT`): JWT of the user

    ## Params
    * `queue_id` (`int`): ID of the queue to delete
    """
    IQueueList,
    delete(
        token,
        f"{URL}/queue_list/delete",
        {
            "queue_id": queue_id,
        }
    )


def queue_edit(token: JWT, queue_id: QueueId, new_name: str):
    """
    ## PUT `/taskboard/queue_list/edit`

    ## Headers
    * `token` (`JWT`): JWT of the user

    ## Body
    * `queue_id` (`int`): the ID of the queue to edit
    * `new_name` (`str`): the new name of the queue
    """
    IQueueList,
    put(
        token,
        f"{URL}/queue_list/edit",
        {
            "queue_id": queue_id,
            "new_name": new_name,
        }
    )
