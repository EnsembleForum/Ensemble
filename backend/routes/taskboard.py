"""
# Backend / Routes / Taskboard

Taskboard-related routes
"""
import json
from flask import Blueprint, request
from backend.models.user import User
from backend.models.queue import Queue
from backend.models.post import Post
from backend.types.identifiers import QueueId, PostId
from backend.types.queue import IQueueFullInfo, IQueueList
from backend.util.tokens import uses_token
from backend.util.validators import assert_valid_str_field
from backend.types.queue import IQueueId
from backend.models.permissions import Permission


taskboard = Blueprint('taskboard', 'taskboard')


@taskboard.get("/queue_list")
@uses_token
def queue_list(user: User, *_) -> IQueueList:
    user.permissions.assert_can(Permission.ViewTaskboard)
    return {"queues": list(map(lambda q: q.basic_info(), Queue.all()))}


@taskboard.post("/queue_list/create")
@uses_token
def queue_create(user: User, *_) -> IQueueId:
    user.permissions.assert_can(Permission.ManageQueues)

    data = json.loads(request.data)
    queue_name: str = data["queue_name"]
    queue_id = Queue.create(queue_name).id

    return {"queue_id": queue_id}


@taskboard.delete("/queue_list/delete")
@uses_token
def queue_delete(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.ManageQueues)

    queue_id: QueueId = QueueId(request.args["queue_id"])
    queue = Queue(queue_id)
    queue.delete()

    return {}


@taskboard.put("/queue_list/edit")
@uses_token
def queue_edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.ManageQueues)

    data = json.loads(request.data)

    queue_id: QueueId = QueueId(data["queue_id"])
    new_name = data['new_name']
    queue = Queue(queue_id)
    assert_valid_str_field(new_name, 'queue_name')
    queue.name = new_name

    return {}


@taskboard.get("/queue/post_list")
@uses_token
def post_list(user: User, *_) -> IQueueFullInfo:
    user.permissions.assert_can(Permission.FollowQueue)
    queue_id: QueueId = QueueId(request.args["queue_id"])
    queue = Queue(queue_id)
    return queue.full_info()


@taskboard.put("/queue/post_add")
@uses_token
def queue_post_add(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.TaskboardDelegate)
    queue_id: QueueId = QueueId(request.args["queue_id"])
    post_id: PostId = PostId(request.args["post_id"])

    post = Post(post_id)
    queue = Queue(queue_id)

    post.queue = queue

    return {}
