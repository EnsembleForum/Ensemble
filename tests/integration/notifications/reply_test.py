"""
# Tests / Integration / Notifications / Reply test

Tests for users getting notifications for replies to posts

* User gets notification when someone comments on their post
* Commenter gets notification if someone replies to their comment
* OP gets notification if someone replies to a comment on their post TODO
* OP doesn't get notification if they comment on their own post TODO
* User doesn't get notification if they reply to their own comment TODO
* OP doesn't get notification if they reply to a comment on their own post TODO
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts
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
    assert notifs == [{
        "notification_id": expect.Any(int),
        "seen": False,
        "heading": f"User commented on your post {make_posts['head1']}",
        "body": "This is a comment",
        'post': make_posts['post1_id'],
        'comment': comment,
        'reply': None,
        'queue': None,
    }]


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
    assert notifs == [{
        "notification_id": expect.Any(int),
        "seen": False,
        "heading": f"User replied to your comment on {make_posts['head1']}",
        "body": "This is a reply",
        'post': make_posts['post1_id'],
        'comment': comment,
        'reply': reply,
        'queue': None,
    }]
