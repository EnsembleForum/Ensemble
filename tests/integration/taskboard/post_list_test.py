"""
# Tests / Integration / Browse / Post list

Tests for post list routes

* Fails with invalid queue_id
* No permission
* Success
"""
import pytest
from backend.types.identifiers import QueueId
from backend.util.http_errors import Forbidden, BadRequest
from tests.integration.request.taskboard import (
    queue_create,
    post_list,
)
from tests.integration.conftest import (
    IAllUsers,
    IMakeQueues,
    IBasicServerSetup,
)


def test_invalid_queue_id(
    basic_server_setup: IBasicServerSetup,
):
    """
    If we are given an invalid queue_id, we get a 400 error
    """
    token = basic_server_setup["token"]
    invalid_queue_id = QueueId(-1)
    with pytest.raises(BadRequest):
        post_list(token, invalid_queue_id)


def test_no_permission(
    all_users: IAllUsers,
    make_queues: IMakeQueues,
):
    """
    Users shouldn't be able to create queues
    """
    with pytest.raises(Forbidden):
        post_list(all_users['users'][0]['token'], make_queues["queue1_id"])


def test_success(
    basic_server_setup: IBasicServerSetup,
    make_queues: IMakeQueues,
):
    """
    Testing that admins can successfully create queues
    """
    token = basic_server_setup["token"]
    queue_name = "queue_name"
    queue_id = queue_create(token, "queue_name")["queue_id"]
    queue = post_list(token, queue_id)
    assert queue["queue_name"] == queue_name
