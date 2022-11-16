"""
# Tests / Integration / Notifications / Queue added test

Tests for notifications when posts get added to a queue

* Mods get notified if a post gets added to a queue they follow
* Mods don't get notified if they were the one doing the adding
* Mods don't get notified if they aren't following the queue
"""
from datetime import datetime
import jestspectation as expect
from ..conftest import (
    ISimpleUsers,
    IMakePosts,
    IDefaultQueues,
    IBasicServerSetup,
)
from ensemble_request import notifications, taskboard


def test_followers_notified(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
    default_queues: IDefaultQueues,
):
    """
    Do mods following a queue get notified when a post is added to the queue?
    """
    taskboard.queue_follow(
        simple_users['mod']['token'],
        default_queues['main'],
    )

    taskboard.queue_post_add(
        simple_users['admin']['token'],
        default_queues['main'],
        make_posts['post1_id'],
    )

    notifs = notifications.list(simple_users['mod']['token'])

    assert notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "timestamp": expect.FloatApprox(
                datetime.now().timestamp(),
                magnitude=2
            ),
            "seen": False,
            "user_from": simple_users['admin']['user_id'],
            "heading": "New post in queue Main",
            "body": make_posts['head1'],
            "post": make_posts['post1_id'],
            "comment": None,
            "reply": None,
            "queue": default_queues['main'],
        },
    ])


def test_non_followers_not_notified(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
    default_queues: IDefaultQueues,
):
    """
    Do mods not following a queue not get notified when a post is added to the
    queue?
    """
    taskboard.queue_post_add(
        basic_server_setup['token'],
        default_queues['main'],
        make_posts['post1_id'],
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []


def test_mover_not_notified(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
    default_queues: IDefaultQueues,
):
    """
    Does the mod who moved the post not get a notification?
    """
    taskboard.queue_follow(
        basic_server_setup['token'],
        default_queues['main'],
    )

    taskboard.queue_post_add(
        basic_server_setup['token'],
        default_queues['main'],
        make_posts['post1_id'],
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []
