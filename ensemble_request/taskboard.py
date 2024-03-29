"""
# Tests / Integration / Request / Taskboard

Helper functions for requesting queue-related code
"""
from typing import cast
from backend.types.queue import IQueueId, IQueueFullInfo, IQueueList
from backend.types.identifiers import QueueId, PostId
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, delete, put


URL = f"{URL}/taskboard"


def queue_list(token: JWT) -> IQueueList:
    """
    ## GET `/taskboard/queue_list`

    Get a list of queues

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Returns
    Object containing:
    * `queues`: list of objects containing:
            * `queue_name` (`str`): the name of the queue
            * `queue_id` (`int`): ID of the queue
            * `view_only` (`bool`): whether this queue is view only
            * `following` (`bool`): whether the user follows this queue

    ## Errors

    ### 403
    * User does not have permission `ViewTaskboard`
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
    * `Authorization` (`JWT`): JWT of the user

    ## Body:
    * `queue_name` (`str`): Name to use for the new queue

    ## Returns
    Object containing:
    * `queue_id` (`int`): ID of the new queue

    ## Errors

    ### 400
    * Empty queue name
    * Duplicate queue name

    ### 403
    * User does not have permission `ManageQueues`
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


def queue_delete(token: JWT, queue_id: QueueId):
    """
    ## DELETE `/taskboard/queue_list/delete`

    Delete a queue

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Params
    * `queue_id` (`int`): ID of the queue to delete

    ## Errors

    ### 400
    * Invalid queue ID

    ### 403
    * User does not have permission `ManageQueues`
    """
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

    Rename a queue.

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `queue_id` (`int`): the ID of the queue to edit
    * `new_name` (`str`): the new name of the queue

    ## Errors

    ### 400
    * Invalid queue ID
    * Empty queue name
    * Duplicate queue name

    ### 403
    * User does not have permission `ManageQueues`
    """
    put(
        token,
        f"{URL}/queue_list/edit",
        {
            "queue_id": queue_id,
            "new_name": new_name,
        }
    )


def queue_post_list(token: JWT, queue_id: QueueId) -> IQueueFullInfo:
    """
    ## GET `/taskboard/queue/post_list`

    Get a detailed info of a queue

    ## Permissions
    * `FollowQueue`

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Params
    * `queue_id` (`int`): ID of the queue to get info on

    ## Returns
    * `queue_id` (`int`): ID of the queue
    * `queue_name` (`str`): name of the queue
    * `posts`: (`list[int]`): list of post IDs in this queue
    * `view_only` (`bool`): whether this queue is view only
    * `following` (`bool`): whether the user follows this queue

    ## Errors

    ### 400
    * Invalid queue ID

    ### 403
    * User does not have permission `FollowQueue`
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


def queue_post_add(token: JWT, queue_id: QueueId, post_id: PostId):
    """
    ## PUT `/taskboard/queue/post_add`

    Move a post to a queue

    ## Permissions
    * `TaskboardDelegate`

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Params
    * `queue_id` (`int`): ID of the queue to send the post to
    * `post_id` (`int`): ID of post whose queue is being changed

    ## Errors

    ### 400
    * Invalid queue ID
    * Cannot move to or from view-only queues

    ### 403
    * User does not have permission `TaskboardDelegate`
    """
    put(
        token,
        f"{URL}/queue/post_add",
        {
            "queue_id": queue_id,
            "post_id": post_id,
        }
    )


def queue_follow(token: JWT, queue_id: QueueId):
    """
    ## PUT `/taskboard/queue/follow`

    Toggle whether you are following a queue. If so, you receive a notification
    whenever a post is moved to a queue.

    ## Permissions
    * `TaskboardDelegate`

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Params
    * `queue_id` (`int`): ID of the queue to follow

    ## Errors

    ### 400
    * Invalid queue ID

    ### 403
    * User does not have permission `QueueFollow`
    """
    put(
        token,
        f"{URL}/queue/follow",
        {
            "queue_id": queue_id,
        }
    )
