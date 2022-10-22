"""
# Tests / Integration / Browse / Queue View

Tests for queue view routes

* Fails with invalid queue_id
* Success with valid queue_id
"""
import pytest
from typing import cast
from backend.types.identifiers import QueueId
from backend.util import http_errors
from tests.integration.request.taskboard import (
    queue_create,
    queue_view,
)


def test_invalid_queue_id(all_users, make_queues):
    """
    If we are given an invalid queue_id, we get a 400 error
    """
    token = all_users["users"][0]["token"]
    invalid_queue_id = (
        max(make_queues["queue1_id"], make_queues["queue2_id"]) + 1
    )

    invalid_queue_id = cast(QueueId, invalid_queue_id)
    print(type(invalid_queue_id), invalid_queue_id, 'hello world')
    with pytest.raises(http_errors.BadRequest):
        print('kms')
        queue_view(token, invalid_queue_id)
        print(type(invalid_queue_id), 'goodbye world')


def test_get_queue_success(all_users):
    """
    Can we get the full details of a valid queue?
    """
    token = all_users["users"][0]["token"]
    queue_name = "queue_name"
    queue_id = queue_create(token, "queue_name")["queue_id"]
    print('type of queue_id is', type(queue_id))
    queue = queue_view(token, queue_id)
    assert queue["queue_name"] == queue_name
