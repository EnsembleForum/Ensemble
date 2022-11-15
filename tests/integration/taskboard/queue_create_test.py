"""
# Tests / Integration / Taskboard / Queue create

Tests for creating queues

* No permission
* Empty name
* Success
"""
import pytest
from backend.util.http_errors import Forbidden, BadRequest
from ensemble_request.taskboard import (
    queue_create,
    queue_post_list,
)
from tests.integration.conftest import (
    ISimpleUsers,
    IBasicServerSetup,
)


def test_no_permission(simple_users: ISimpleUsers):
    """
    Testing that when users try to create or delete queues it will fail
    """
    with pytest.raises(Forbidden):
        queue_create(simple_users['user']['token'], "queue3_name")


def test_empty_name(basic_server_setup: IBasicServerSetup):
    """
    Do we get a bad request if the queue name is empty
    """
    with pytest.raises(BadRequest):
        queue_create(basic_server_setup['token'], "")


@pytest.mark.core
def test_success(basic_server_setup: IBasicServerSetup):
    """
    Can we create a queue
    """
    queue = queue_create(basic_server_setup['token'], "my queue")
    details = queue_post_list(basic_server_setup['token'], queue['queue_id'])
    assert details['queue_name'] == "my queue"


def test_name_alr_exists(basic_server_setup: IBasicServerSetup):
    """
    Do we get a bad request if the queue name already exists
    """
    queue_name = "my queue"
    queue_create(basic_server_setup['token'], queue_name)
    with pytest.raises(BadRequest):
        queue_create(basic_server_setup['token'], queue_name)
