"""
# Tests / Integration / Browse / Default Queue

Tests for the default queue

* Is it created when the server is initialised
* It should be impossible to delete
* All new posts are added to the default queue
"""
import pytest
from backend.util.http_errors import BadRequest
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

# Helper function to get main queue


def get_main_queue(queues):
    for q in queues:
        if q["queue_name"] == "Main queue":
            return q


def test_default_queue_create(basic_server_setup: IBasicServerSetup):
    queues = queue_list(basic_server_setup['token'])['queues']
    assert len(queues) == 2
    queue_names = sorted([q['queue_name'] for q in queues])
    assert queue_names == sorted(["Main queue", "Answered queue"])


def test_default_queue_cannot_delete(basic_server_setup: IBasicServerSetup):
    default_queue = queue_list(basic_server_setup['token'])['queues'][0]
    with pytest.raises(BadRequest):
        queue_delete(basic_server_setup['token'], default_queue['queue_id'])


def test_new_post_default(basic_server_setup: IBasicServerSetup):
    token = basic_server_setup['token']
    default_queue = get_main_queue(queue_list(token)['queues'])
    posts = queue_post_list(token, default_queue['queue_id'])['posts']
    assert len(posts) == 0
    post_create(token, 'first_post', 'post_content', [])
    posts = queue_post_list(token, default_queue['queue_id'])['posts']
    assert len(posts) == 1
