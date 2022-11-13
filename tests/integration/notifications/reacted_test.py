"""
# Tests / Integration / Notifications / React test

Tests for notifications when reacting to content

* Notified of react to post
* Notified of react to comment
* Notified of react to reply
* Not notified of own reaction to post
* Not notified of own reaction to comment
* Not notified of own reaction to reply
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_notified_post(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users receive a notification when someone reacts to their post?
    """
    browse.post_react(simple_users['user']['token'], make_posts['post1_id'])

    assert (
        notifications.list(simple_users['admin']['token'])['notifications']
        == [{
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": None,
            "heading": "Your post received a me too",
            "body": make_posts['head1'],
            "post": make_posts['post1_id'],
            "comment": None,
            "reply": None,
            "queue": None,
        }]
    )


def test_notified_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users receive a notification when someone reacts to their comment?
    """
    comment = browse.add_comment(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    browse.comment_react(simple_users['user']['token'], comment)

    assert (
        notifications.list(simple_users['admin']['token'])['notifications']
        == [{
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": None,
            "heading": "Your comment received thanks",
            "body": "This is a comment",
            "post": make_posts['post1_id'],
            "comment": comment,
            "reply": None,
            "queue": None,
        }]
    )


def test_notified_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do users receive a notification when someone reacts to their reply?
    """
    comment = browse.add_comment(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    reply = browse.add_reply(
        simple_users['admin']['token'],
        comment,
        "This is a reply",
    )['reply_id']
    browse.reply_react(simple_users['user']['token'], reply)

    assert (
        notifications.list(simple_users['admin']['token'])['notifications']
        == [{
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": None,
            "heading": "Your reply received thanks",
            "body": "This is a reply",
            "post": make_posts['post1_id'],
            "comment": comment,
            "reply": reply,
            "queue": None,
        }]
    )


def test_not_notified_own_post(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Do users not receive a notification when they react to their own post?
    """
    browse.post_react(basic_server_setup['token'], make_posts['post1_id'])

    assert (
        notifications.list(basic_server_setup['token'])['notifications']
        == []
    )


def test_not_notified_own_comment(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Do users not receive a notification when reacting to their own comment?
    """
    comment = browse.add_comment(
        basic_server_setup['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    browse.comment_react(basic_server_setup['token'], comment)

    assert (
        notifications.list(basic_server_setup['token'])['notifications']
        == []
    )


def test_not_notified_own_reply(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Do users not receive a notification when reacting to their own reply?
    """
    comment = browse.add_comment(
        basic_server_setup['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']
    reply = browse.add_reply(
        basic_server_setup['token'],
        comment,
        "This is a reply",
    )['reply_id']
    browse.reply_react(basic_server_setup['token'], reply)

    assert (
        notifications.list(basic_server_setup['token'])['notifications']
        == []
    )
