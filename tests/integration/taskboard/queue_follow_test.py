"""
# Tests / Integration / Taskboard / Queue follow test

Tests for following queues

Note that this does not test the notifications associated with this. For that,
refer to tests/integration/notifications/queue_added_test.py

* Users can follow queues
* Users can unfollow queues
* Bad request for invalid queue ID
* Forbidden for permission error
"""
import pytest
from ..conftest import IDefaultQueues, IBasicServerSetup, ISimpleUsers
from backend.util import http_errors
from backend.types.identifiers import QueueId
from ensemble_request import taskboard


@pytest.mark.core
def test_follow_queue(
    basic_server_setup: IBasicServerSetup,
    default_queues: IDefaultQueues,
):
    """
    Users can follow queues
    """
    taskboard.queue_follow(
        basic_server_setup['token'],
        default_queues['main'],
    )
    assert taskboard.queue_post_list(
        basic_server_setup['token'],
        default_queues['main'],
    )['following']


def test_unfollow_queue(
    basic_server_setup: IBasicServerSetup,
    default_queues: IDefaultQueues,
):
    """
    Users can follow queues
    """
    taskboard.queue_follow(
        basic_server_setup['token'],
        default_queues['main'],
    )
    taskboard.queue_follow(
        basic_server_setup['token'],
        default_queues['main'],
    )
    assert not taskboard.queue_post_list(
        basic_server_setup['token'],
        default_queues['main'],
    )['following']


def test_cant_follow_invalid_queue(basic_server_setup: IBasicServerSetup):
    """Error if we try to follow an invalid queue"""
    with pytest.raises(http_errors.BadRequest):
        taskboard.queue_follow(basic_server_setup['token'], QueueId(-1))


def test_cant_follow_no_permission(
    simple_users: ISimpleUsers,
    default_queues: IDefaultQueues,
):
    """Error if we try to follow an invalid queue"""
    with pytest.raises(http_errors.Forbidden):
        taskboard.queue_follow(
            simple_users['user']['token'],
            default_queues['main']
        )
