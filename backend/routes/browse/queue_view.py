"""
# Backend / Routes / Browse / Post View

Post View routes
"""
import json
from flask import Blueprint, request
from typing import cast
from backend.models.queue import Queue
from backend.types.identifiers import PostId, QueueId
from backend.types.queue import IQueueFullInfo
from backend.util import http_errors
from backend.util.tokens import uses_token

queue_view = Blueprint("queue_view", "queue_view")


@queue_view.get("")
@uses_token
def get_queue(*_) -> IQueueFullInfo:
    """
    Get the list of available queues

    ## Body:

    ## Returns:
    * `queues`: [queue_id:int, queue_name: str]
    """
    queue_id: QueueId = cast(QueueId, request.args["queue_id"])
    queue = Queue(queue_id)
    return queue.full_info
