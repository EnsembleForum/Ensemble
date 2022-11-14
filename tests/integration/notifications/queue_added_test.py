"""
# Tests / Integration / Notifications / Queue added test

Tests for notifications when posts get added to a queue

* Mods get notified if a post gets added to a queue they follow
* Mods don't get notified if they were the one doing the adding
* Mods don't get notified if they aren't following the queue
"""
import pytest
import jestspectation as expect
from ..conftest import (
    ISimpleUsers,
    IMakePosts,
    IMakeQueues,
    IBasicServerSetup,
)
from ensemble_request import notifications, taskboard


# No way to follow queues
@pytest.mark.xfail
def test_followers_notified(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
    make_queues: IMakeQueues,
):
    """
    Do mods following a queue get notified when a post is added to the queue?
    """
    taskboard.follow_queue(  # type: ignore
        simple_users['mod']['token'],
        make_queues['queue1_id'],
    )

    taskboard.queue_post_add(
        simple_users['admin']['token'],
        make_queues['queue1_id'],
        make_posts['post1_id'],
    )

    notifs = notifications.list(simple_users['admin']['token'])

    assert notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": f"New post in queue {make_queues['queue_name1']}",
            "body": make_posts['head1'],
            "post": make_posts['post1_id'],
            "comment": None,
            "reply": None,
            "queue": make_queues['queue1_id'],
        },
    ]


def test_non_followers_not_notified(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
    make_queues: IMakeQueues,
):
    """
    Do mods not following a queue not get notified when a post is added to the
    queue?
    """
    taskboard.queue_post_add(
        basic_server_setup['token'],
        make_queues['queue1_id'],
        make_posts['post1_id'],
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []


# No way to follow queues
@pytest.mark.xfail
def test_mover_not_notified(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
    make_queues: IMakeQueues,
):
    """
    Does the mod who moved the post not get a notification?
    """
    taskboard.follow_queue(  # type: ignore
        basic_server_setup['token'],
        make_queues['queue1_id'],
    )

    taskboard.queue_post_add(
        basic_server_setup['token'],
        make_queues['queue1_id'],
        make_posts['post1_id'],
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []
