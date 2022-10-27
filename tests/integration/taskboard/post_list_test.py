"""
# Tests / Integration / Browse / Post list

Tests for post list routes

* Fails with invalid queue_id
* Success with valid queue_id
"""
import pytest
from typing import cast
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
    make_queues: IMakeQueues,
):
    """
    If we are given an invalid queue_id, we get a 400 error
    """
    token = basic_server_setup["token"]
    invalid_queue_id = (
        max(make_queues["queue1_id"], make_queues["queue2_id"]) + 1
    )

    invalid_queue_id = cast(QueueId, invalid_queue_id)
    with pytest.raises(BadRequest):
        post_list(token, invalid_queue_id)


def test_get_queue_success(basic_server_setup: IBasicServerSetup):
    """
    Testing that admins can successfully create queues
    """
    token = basic_server_setup["token"]
    queue_name = "queue_name"
    queue_id = queue_create(token, "queue_name")["queue_id"]
    queue = post_list(token, queue_id)
    assert queue["queue_name"] == queue_name


def test_queue_permissions_fail(all_users: IAllUsers):
    """
    Testing that when users try to create or delete queues it will fail
    """
    admin_token1 = all_users['admins'][0]['token']
    admin_token2 = all_users['admins'][1]['token']
    user_token1 = all_users['users'][0]['token']

    queue1 = queue_create(admin_token1, "queue1_name")
    queue2 = queue_create(admin_token2, "queue2_name")

    queue1_id = queue1["queue_id"]
    queue2_id = queue2["queue_id"]

    assert queue1_id == 1
    assert queue2_id == 2

    # Should raise an error but currently does not
    with pytest.raises(Forbidden):
        queue_create(user_token1, "queue3_name")
