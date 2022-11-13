"""
# Tests / Integration / Browse / Default Queue

Tests for the default queue

* Is it created when the server is initialised
* It should be impossible to delete
* All new posts are added to the default queue
"""
import pytest
from backend.util.http_errors import BadRequest
from tests.integration.helpers import get_queue
from ensemble_request.taskboard import (
    queue_post_list,
    queue_list,
    queue_delete,
)
from ensemble_request.browse import (
    post_create
)
from tests.integration.conftest import (
    IBasicServerSetup,
)


def test_default_queue_create(basic_server_setup: IBasicServerSetup):
    """
    Test that the 3 default queues are created on forum initialisation
    """
    queues = queue_list(basic_server_setup['token'])['queues']
    assert len(queues) == 3
    queue_names = sorted([q['queue_name'] for q in queues])
    assert queue_names == sorted(
        ["Main queue", "Answered queue", "Closed queue", "Deleted queue"])


def test_default_queue_cannot_delete(basic_server_setup: IBasicServerSetup):
    """
    Fails when trying to delete an immutable queue
    """
    default_queues = queue_list(basic_server_setup['token'])['queues']
    # All queues created during forum initialisation are immutable
    for queue in default_queues:
        with pytest.raises(BadRequest):
            queue_delete(basic_server_setup['token'], queue['queue_id'])


def test_new_post_default(basic_server_setup: IBasicServerSetup):
    """
    Test that posts are in the main queue by default when created
    """
    token = basic_server_setup['token']
    default_queue = get_queue(queue_list(token)['queues'], "Main queue")
    posts = queue_post_list(token, default_queue['queue_id'])['posts']
    assert len(posts) == 0
    post_create(token, 'first_post', 'post_content', [])
    posts = queue_post_list(token, default_queue['queue_id'])['posts']
    assert len(posts) == 1


def test_view_only_basic_info(basic_server_setup: IBasicServerSetup):
    """
    Whether queue_list correctly shows that the queue is view_only or not
    """
    token = basic_server_setup['token']
    queues = queue_list(token)['queues']

    assert not get_queue(queues, "Main queue")["view_only"]
    assert get_queue(queues, "Answered queue")["view_only"]
    assert get_queue(queues, "Closed queue")["view_only"]
    assert get_queue(queues, "Deleted queue")["view_only"]


def test_view_only_ful_info(basic_server_setup: IBasicServerSetup):
    """
    Whether queue__post_list correctly shows that the queue is view_only or not
    """
    token = basic_server_setup['token']
    queues = queue_list(token)['queues']
    main_id = get_queue(queues, "Main queue")["queue_id"]
    answered_id = get_queue(queues, "Answered queue")["queue_id"]
    closed_id = get_queue(queues, "Closed queue")["queue_id"]
    deleted_id = get_queue(queues, "Deleted queue")["queue_id"]

    assert not queue_post_list(token, main_id)["view_only"]
    assert queue_post_list(token, answered_id)["view_only"]
    assert queue_post_list(token, closed_id)["view_only"]
    assert queue_post_list(token, deleted_id)["view_only"]
