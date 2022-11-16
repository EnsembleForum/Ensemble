"""
# Backend / Routes / Taskboard

Taskboard-related routes
"""
import json
from flask import Blueprint, request
from backend.models import User, Queue, Post, Permission
from backend.models.notifications import NotificationQueueAdded
from backend.types.identifiers import QueueId, PostId
from backend.types.queue import IQueueFullInfo, IQueueList
from backend.util.tokens import uses_token
from backend.util.validators import assert_valid_str_field
from backend.types.queue import IQueueId
from backend.util import http_errors


taskboard = Blueprint('taskboard', 'taskboard')


@taskboard.get("/queue_list")
@uses_token
def queue_list(user: User, *_) -> IQueueList:
    user.permissions.assert_can(Permission.ViewTaskboard)
    return {"queues": list(map(lambda q: q.basic_info(user), Queue.all()))}


@taskboard.post("/queue_list/create")
@uses_token
def queue_create(user: User, *_) -> IQueueId:
    user.permissions.assert_can(Permission.ManageQueues)

    data = json.loads(request.data)
    queue_name = data["queue_name"]
    queue_id = Queue.create(queue_name).id

    return {"queue_id": queue_id}


@taskboard.delete("/queue_list/delete")
@uses_token
def queue_delete(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.ManageQueues)

    queue_id = QueueId(request.args["queue_id"])
    queue = Queue(queue_id)
    queue.delete()

    return {}


@taskboard.put("/queue_list/edit")
@uses_token
def queue_edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.ManageQueues)

    data = json.loads(request.data)

    queue_id = QueueId(data["queue_id"])
    new_name = data['new_name']
    queue = Queue(queue_id)
    assert_valid_str_field(new_name, 'queue_name')
    queue.name = new_name

    return {}


@taskboard.get("/queue/post_list")
@uses_token
def post_list(user: User, *_) -> IQueueFullInfo:
    user.permissions.assert_can(Permission.FollowQueue)
    queue_id = QueueId(request.args["queue_id"])
    queue = Queue(queue_id)
    return queue.full_info(user)


@taskboard.put("/queue/post_add")
@uses_token
def queue_post_add(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.TaskboardDelegate)
    data = json.loads(request.data)
    queue_id = QueueId(data["queue_id"])
    post_id = PostId(data["post_id"])

    post = Post(post_id)
    queue = Queue(queue_id)

    if queue.view_only or post.queue.view_only:
        raise http_errors.BadRequest(
            "Cannot move post to and from view only queues"
        )

    post.queue = queue

    for u in queue.get_followers():
        if u != user:
            NotificationQueueAdded.create(
                u,
                user,
                post,
                queue,
            )

    return {}


@taskboard.put("/queue/follow")
@uses_token
def queue_follow(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.FollowQueue)
    data = json.loads(request.data)
    queue_id = QueueId(data["queue_id"])
    Queue(queue_id).follow(user)
    return {}
