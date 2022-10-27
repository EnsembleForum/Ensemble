"""
# Backend / Routes / Taskboard

Taskboard-related routes
"""
import json
from flask import Blueprint, request
from backend.models.user import User
from typing import cast
from backend.models.queue import Queue
from backend.types.identifiers import QueueId
from backend.types.queue import IQueueFullInfo, IQueueList
from backend.util.tokens import uses_token
from backend.types.queue import IQueueId
from backend.models.permissions import Permission


taskboard = Blueprint('taskboard', 'taskboard')


@taskboard.get("/queue_list")
@uses_token
def queue_list(user: User, *_) -> IQueueList:
    """
    Returns a list of available queues

    ## Body:
    * `queue_name` (`str`): name of queue

    ## Returns:
    * `IQueueId`: identifier of the post
    """
    user.permissions.assert_can(Permission.ManageQueues)
    return {"queues": list(map(lambda q: q.basic_info(), Queue.all()))}


@taskboard.post("/queue_list/create")
@uses_token
def queue_create(user: User, *_) -> IQueueId:
    """
    Create a queue

    ## Body:
    * `queue_name` (`str`): name of queue

    ## Returns:
    * `IQueueId`: identifier of the post
    """
    user.permissions.assert_can(Permission.ManageQueues)

    data = json.loads(request.data)
    queue_name: str = data["queue_name"]
    queue_id = Queue.create(queue_name).id

    return {"queue_id": queue_id}


@taskboard.delete("/queue_list/delete")
@uses_token
def queue_delete(user: User, *_) -> dict:
    """
    Delete a queue

    ## Args:
    * `queue_id` (`int`): queue to delete
    """
    # HERE
    user.permissions.assert_can(Permission.ManageQueues)

    queue_id: QueueId = cast(QueueId, request.args["queue_id"])
    queue = Queue(queue_id)
    queue.delete()

    return {}


@taskboard.get("/queue/post_list")
@uses_token
def post_list(user: User, *_) -> IQueueFullInfo:
    """
    Get list of posts in a queue

    ## Body:
    * `queue_id`: Queue ID

    ## Returns:
    * `queues`: [queue_id:int, queue_name: str]
    """
    queue_id: QueueId = cast(QueueId, int(request.args["queue_id"]))
    queue = Queue(queue_id)

    user.permissions.assert_can(Permission.ManageQueues)
    return queue.full_info()
