"""
# Tests / Integration / Notifications / Routes test

Tests for notification routes

* Initially, user doesn't have notifications
* Marking a notification as seen works correctly
* Marking a notification as unseen works correctly
* Can't mark info for other user's notifications
* BadRequest for invalid notification ID
"""
import pytest
from backend.types.identifiers import NotificationId
from backend.util import http_errors
from ..conftest import IBasicServerSetup, ISimpleUsers, IMakePosts
from ensemble_request import notifications, browse


def test_no_notifs_default(basic_server_setup: IBasicServerSetup):
    """Do users have no notifications by default?"""
    assert len(
        notifications.list(basic_server_setup['token'])['notifications']) == 0


def test_see_notification(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """Can we mark a notification as seen?"""
    # Comment on the post
    browse.add_comment(
        simple_users['user']['token'],
        make_posts['post1_id'],
        "My reply",
    )
    # OP should get a notification
    n = notifications.list(simple_users['admin']['token'])['notifications'][0]
    # Mark it as seen
    notifications.seen(
        simple_users['admin']['token'],
        n['notification_id'],
        True,
    )
    n = notifications.list(simple_users['admin']['token'])['notifications'][0]
    assert n['seen']


def test_unseen_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Can we mark a notification as seen?"""
    # Comment on the post
    browse.add_comment(
        simple_users['user']['token'],
        make_posts['post1_id'],
        "My reply",
    )
    # OP should get a notification
    n = notifications.list(simple_users['admin']['token'])['notifications'][0]
    # Mark it as seen the unseen
    notifications.seen(
        simple_users['admin']['token'],
        n['notification_id'],
        True,
    )
    notifications.seen(
        simple_users['admin']['token'],
        n['notification_id'],
        False,
    )
    n = notifications.list(simple_users['admin']['token'])['notifications'][0]
    assert not n['seen']


def test_see_notification_wrong_user(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do we get an error if we try to see a notification from the wrong user?
    """
    # Comment on the post
    browse.add_comment(
        simple_users['user']['token'],
        make_posts['post1_id'],
        "My reply",
    )
    # OP should get a notification
    n = notifications.list(simple_users['admin']['token'])['notifications'][0]
    # Mark it as seen with the wrong user
    with pytest.raises(http_errors.Forbidden):
        notifications.seen(
            simple_users['user']['token'],
            n['notification_id'],
            True,
        )


def test_see_notification_invalid_id(basic_server_setup: IBasicServerSetup):
    """Do we get an error if we try to see a notification with an invalid ID?
    """
    with pytest.raises(http_errors.BadRequest):
        notifications.seen(
            basic_server_setup['token'],
            NotificationId(-1),
            True,
        )
