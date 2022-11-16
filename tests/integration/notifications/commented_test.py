"""
# Tests / Integration / Notifications / Reply test

Tests for users getting notifications for replies to posts

* User gets notification when someone comments on their post
* Commenter gets notification if someone replies to their comment
* OP gets notification if someone replies to a comment on their post
* OP doesn't get notification if they comment on their own post
* User doesn't get notification if they reply to their own comment
* OP doesn't get notification if they reply to a comment on their own post TODO
"""
from datetime import datetime
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_notification_on_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get a notification when someone comments on their post?"""
    comment = browse.comment.create(
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
        "timestamp": expect.FloatApprox(
            datetime.now().timestamp(),
            magnitude=2
        ),
        "user_from": simple_users['user']['user_id'],
        "heading": "New comment on your post",
        "body": "This is a comment",
        'post': make_posts['post1_id'],
        'comment': comment,
        'reply': None,
        'queue': None,
    }]


def test_notification_on_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users get a notification when someone replies to their comment on
    a post?
    """
    comment = browse.comment.create(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    reply = browse.reply.create(
        simple_users['user']['token'],
        comment,
        "This is a reply",
    )['reply_id']
    # Mod should have gotten a notification
    notifs = notifications.list(simple_users['mod']['token'])['notifications']
    assert notifs == [{
        "notification_id": expect.Any(int),
        "seen": False,
        "timestamp": expect.FloatApprox(
            datetime.now().timestamp(),
            magnitude=2
        ),
        "user_from": simple_users['user']['user_id'],
        "heading": "New reply to your comment",
        "body": "This is a reply",
        'post': make_posts['post1_id'],
        'comment': comment,
        'reply': reply,
        'queue': None,
    }]


def test_reply_op_notified(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does OP get a notification when someone replies to a comment on their post
    """
    comment = browse.comment.create(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    reply = browse.reply.create(
        simple_users['user']['token'],
        comment,
        "This is a reply",
    )['reply_id']
    # Admin should have gotten a notification
    notifs = notifications.list(simple_users['admin']['token'])[
        'notifications']
    assert notifs[0] == {
        "notification_id": expect.Any(int),
        "seen": False,
        "timestamp": expect.FloatApprox(
            datetime.now().timestamp(),
            magnitude=2
        ),
        "user_from": simple_users['user']['user_id'],
        "heading": "New reply on your post",
        "body": "This is a reply",
        'post': make_posts['post1_id'],
        'comment': comment,
        'reply': reply,
        'queue': None,
    }


def test_no_notification_on_self_comment(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they comment on their own post?"""
    browse.comment.create(
        basic_server_setup['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    # Notifications
    notifs = notifications.list(
        basic_server_setup['token'])['notifications']
    assert notifs == []


def test_no_notifications_on_self_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users not get notified if they reply to their own comment?
    """
    comment = browse.comment.create(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    browse.reply.create(
        simple_users['mod']['token'],
        comment,
        "This is a reply",
    )['reply_id']
    # Mod should have gotten a notification
    notifs = notifications.list(simple_users['mod']['token'])['notifications']
    assert notifs == []


def test_no_notification_on_reply_to_comment_on_own_post(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users not get notified if they reply to a comment on their own post?
    """
    comment = browse.comment.create(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    browse.reply.create(
        simple_users['admin']['token'],
        comment,
        "This is a reply",
    )['reply_id']
    # Mod should have only gotten first notification
    notifs = notifications.list(simple_users['mod']['token'])['notifications']
    assert len(notifs) == 1
