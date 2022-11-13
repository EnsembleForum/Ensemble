"""
# Tests / Integration / Task Board / Queue Delete

Tests for the deleting queues

* Invalid ID
* No permission
* Delete queue success
"""
import pytest
from backend.types.identifiers import QueueId
from backend.util.http_errors import BadRequest, Forbidden
from ensemble_request.taskboard import (
    queue_list,
    queue_delete,
)
from tests.integration.conftest import (
    IBasicServerSetup,
    ISimpleUsers,
    IMakeQueues,
)


def test_no_permission(
    simple_users: ISimpleUsers,
    make_queues: IMakeQueues,
):
    """Test that we can't delete queues without permission"""
    user_token = simple_users['user']['token']
    with pytest.raises(Forbidden):
        queue_delete(user_token, make_queues['queue1_id'])


def test_invalid_id(basic_server_setup: IBasicServerSetup):
    """Test that we get an error if we give an invalid ID"""
    with pytest.raises(BadRequest):
        queue_delete(basic_server_setup['token'], QueueId(-1))


@pytest.mark.core
def test_success(
    basic_server_setup: IBasicServerSetup,
    make_queues: IMakeQueues,
):
    """Queue gets deleted"""
    token = basic_server_setup['token']
    queue_delete(token, make_queues['queue1_id'])
    # Main queue, Answered queue, Closed queue, and make_queues[2]
    assert len(queue_list(token)['queues']) == 4
