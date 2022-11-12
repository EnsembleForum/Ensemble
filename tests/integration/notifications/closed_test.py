"""
# Tests / Integration / Notifications / Closed test

Tests for notifications when closing posts

* Users get notified when their post is closed
* User doesn't get notified if they close their own post
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_closed_post_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their posts are closed?"""
    browse.close_post(simple_users['mod']['token'], make_posts['post1_id'])

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": f"A moderator closed your post {make_posts['head1']}",
            "body": "",
            'post': make_posts['post1_id'],
            'comment': None,
            'reply': None,
            'queue': None,
        },
    ]


def test_reopened_post_no_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users not get notified if their post is reopened?"""
    browse.close_post(simple_users['mod']['token'], make_posts['post1_id'])
    browse.close_post(simple_users['mod']['token'], make_posts['post1_id'])

    notifs = notifications.list(simple_users['admin']['token'])
    # Only the notification for closing
    assert len(notifs['notifications']) == 1


def test_self_closed_post_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they close their own post?"""
    browse.close_post(basic_server_setup['token'], make_posts['post1_id'])

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []
