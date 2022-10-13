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
from backend.types.queue import IQueueFullInfo
from backend.util.tokens import uses_token
from backend.types.queue import IQueueId


taskboard = Blueprint('auth', 'auth')


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
    data = json.loads(request.data)
    queue_name: str = data["queue_name"]

    queue_id = Queue.create(queue_name).id

    return {"queue_id": queue_id}


@uses_token
def queue_delete(user: User, *_) -> IQueueId:
    """
    Create a post

    ## Body:
    * `token` (`JWT`): JWT of the user
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags attached to the new post (ignore for sprint 1)

    ## Returns:
    * `IPostId`: identifier of the post
    """
    data = json.loads(request.data)
    queue_name: str = data["queue_name"]

    queue_id = Queue.create(queue_name).id

    return {"queue_id": queue_id}


@taskboard.get("/queue/post_list")
@uses_token
def post_list(*_) -> IQueueFullInfo:
    """
    Get list of posts in a queue

    ## Body:
    * `queue_id`: Queue ID

    ## Returns:
    * `queues`: [queue_id:int, queue_name: str]
    """
    queue_id: QueueId = cast(QueueId, request.args["queue_id"])
    queue = Queue(queue_id)
    return queue.full_info()
