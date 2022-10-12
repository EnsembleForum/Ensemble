"""
# Backend / Routes / Browse / Post View

Post View routes
"""
import json
from flask import Blueprint, request
from typing import cast
from backend.models.queue import Queue
from backend.types.identifiers import PostId, QueueId
from backend.types.post import IPostFullInfo, IPostId
from backend.util import http_errors
from backend.util.tokens import uses_token

queue_view = Blueprint("queue_view", "queue_view")


@queue_view.get("")
@uses_token
def get_queue(*_) -> IPostFullInfo:
    """
    Get the detailed info of a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostFullInfo`: Dictionary containing full info a post
    """
    queue_id: QueueId = cast(QueueId, request.args["queue_id"])
    queue = Queue(queue_id)
    return queue.full_info
