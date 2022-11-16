"""
# Tests / Integration / Notifications / Closed test

Tests for notifications when closing posts

* Users get notified when their post is closed
* User doesn't get notified if they close their own post
"""
from datetime import datetime
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_closed_post_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their posts are closed?"""
    browse.post.close(simple_users['mod']['token'], make_posts['post1_id'])

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "timestamp": expect.FloatApprox(
                datetime.now().timestamp(),
                magnitude=2
            ),
            "user_from": None,
            "heading": "A mod closed your post",
            "body": make_posts['head1'],
            'post': make_posts['post1_id'],
            'comment': None,
            'reply': None,
            'queue': None,
        },
    ])


def test_reopened_post_no_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users not get notified if their post is reopened?"""
    browse.post.close(simple_users['mod']['token'], make_posts['post1_id'])
    browse.post.close(simple_users['mod']['token'], make_posts['post1_id'])

    notifs = notifications.list(simple_users['admin']['token'])
    # Only the notification for closing
    assert len(notifs['notifications']) == 1


def test_self_closed_post_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they close their own post?"""
    browse.post.close(basic_server_setup['token'], make_posts['post1_id'])

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []
