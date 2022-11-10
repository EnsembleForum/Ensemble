"""
# Tests / Integration / Notifications / Reply test

Tests for users getting notifications for replies to posts

* User gets notification when someone comments on their post
* Commenter gets notification if someone replies to their comment
* OP gets notification if someone replies to a comment on their post
* OP doesn't get notification if they comment on their own post
* User doesn't get notification if they reply to their own comment
* OP doesn't get notification if they reply to a comment on their own post
"""
import pytest
from backend.types.identifiers import NotificationId
from backend.util import http_errors
from ..conftest import IBasicServerSetup, ISimpleUsers, IMakePosts
from ensemble_request import notifications, browse


def test_notification_on_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get a notification when someone comments on their post?"""
    comment = browse.add_comment(
        simple_users['user']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    # Admin should have gotten a notification
    notifs = notifications.list(
        simple_users['admin']['token'])['notifications']
    assert len(notifs) == 1
    assert notifs[0]['seen'] is False
    assert notifs[0]['heading'] \
        == f"Mod commented on your post {make_posts['head1']}"
    assert notifs[0]['body'] == "This is a comment"
    assert notifs[0]['post'] == make_posts['post1_id']
    assert notifs[0]['comment'] == comment
    assert notifs[0]['reply'] is None
    assert notifs[0]['queue'] is None


def test_notifications_on_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users get a notification when someone replies to their comment on
    a post?
    """
    comment = browse.add_comment(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    reply = browse.add_reply(
        simple_users['user']['token'],
        comment,
        "This is a reply",
    )['reply_id']
    # Mod should have gotten a notification
    notifs = notifications.list(simple_users['mod']['token'])['notifications']
    assert len(notifs) == 1
    assert isinstance(notifs[0]['notification_id'], int)
    assert notifs[0]['seen'] is False
    assert notifs[0]['heading'] \
        == f"User replied to your comment on {make_posts['head1']}"
    assert notifs[0]['body'] == "This is a reply"
    assert notifs[0]['post'] == make_posts['post1_id']
    assert notifs[0]['comment'] == comment
    assert notifs[0]['reply'] is reply
    assert notifs[0]['queue'] is None
