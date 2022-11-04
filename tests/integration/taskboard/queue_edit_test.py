"""
# Tests / Integration / Taskboard / Queue edit test

Tests for editing queues

* No permission
* Invalid ID
* Empty name
* Success
"""
import pytest
from backend.types.identifiers import QueueId
from backend.util.http_errors import Forbidden, BadRequest
from ensemble_request.taskboard import (
    post_list,
    queue_edit,
)
from tests.integration.conftest import (
    ISimpleUsers,
    IBasicServerSetup,
    IMakeQueues
)


def test_no_permission(simple_users: ISimpleUsers, make_queues: IMakeQueues):
    """Do we fail if we don't have permission"""
    with pytest.raises(Forbidden):
        queue_edit(
            simple_users['user']['token'],
            make_queues['queue1_id'],
            "Sneaky student renamed this"
        )


def test_invalid_id(basic_server_setup: IBasicServerSetup):
    """Do we fail if we use an invalid ID"""
    with pytest.raises(BadRequest):
        queue_edit(
            basic_server_setup['token'],
            QueueId(-1),
            "New name",
        )


def test_empty_name(
    basic_server_setup: IBasicServerSetup,
    make_queues: IMakeQueues,
):
    """Do we fail if we use an empty name"""
    with pytest.raises(BadRequest):
        queue_edit(
            basic_server_setup['token'],
            make_queues['queue1_id'],
            "",
        )


def test_success(
    basic_server_setup: IBasicServerSetup,
    make_queues: IMakeQueues,
):
    """Do we fail if we use an empty name"""
    queue_edit(
        basic_server_setup['token'],
        make_queues['queue1_id'],
        "My new queue name",
    )
    assert post_list(
        basic_server_setup['token'],
        make_queues['queue1_id'],
    )['queue_name'] == "My new queue name"