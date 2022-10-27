"""
# Tests / Integration / Taskboard / Queue create

Tests for creating queues

* No permission
* Empty name
* Success
"""
import pytest
from backend.util.http_errors import Forbidden, BadRequest
from request.taskboard import (
    queue_create,
    post_list,
)
from tests.integration.conftest import (
    IAllUsers,
    IBasicServerSetup,
)


def test_no_permission(all_users: IAllUsers):
    """
    Testing that when users try to create or delete queues it will fail
    """
    with pytest.raises(Forbidden):
        queue_create(all_users['users'][0]['token'], "queue3_name")


def test_empty_name(basic_server_setup: IBasicServerSetup):
    """
    Do we get a bad request if the queue name is empty
    """
    with pytest.raises(BadRequest):
        queue_create(basic_server_setup['token'], "")


def test_success(basic_server_setup: IBasicServerSetup):
    """
    Can we create a queue
    """
    queue = queue_create(basic_server_setup['token'], "my queue")
    details = post_list(basic_server_setup['token'], queue['queue_id'])
    assert details['queue_name'] == "my queue"
