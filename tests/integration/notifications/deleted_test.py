"""
# Tests / Integration / Notifications / Deleted test

Tests for notifications when deleting posts

* Users get notified when their post is deleted
* User doesn't get notified if they delete their own post
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_deleted_post_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their posts are deleted?"""
    browse.post.delete(simple_users['mod']['token'], make_posts['post1_id'])

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "user_from": None,
            "timestamp": expect.Any(int),
            "seen": False,
            "heading": "Your post was deleted",
            "body": make_posts['head1'],
            'post': make_posts['post1_id'],
            'comment': None,
            'reply': None,
            'queue': None,
        },
    ])


def test_self_deleted_post_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they delete their own post?"""
    browse.post.delete(basic_server_setup['token'], make_posts['post1_id'])

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []


def test_deleted_comment_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their comments are deleted?"""
    comment = browse.comment.create(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    browse.comment.delete(  # type: ignore
        simple_users['mod']['token'],
        comment,
    )

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "timestamp": expect.Any(int),
            "user_from": None,
            "seen": False,
            "heading": "Your comment was deleted",
            "body": "[Deleted]",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ])


def test_self_deleted_comment_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they delete their own comment?"""
    comment = browse.comment.create(
        basic_server_setup['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    browse.comment.delete(  # type: ignore
        basic_server_setup['token'],
        comment,
    )

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []


def test_deleted_reply_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their replies are deleted?"""
    comment = browse.comment.create(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    reply = browse.reply.create(
        simple_users['admin']['token'],
        comment,
        'This is a reply',
    )['reply_id']

    browse.reply.delete(  # type: ignore
        simple_users['mod']['token'],
        reply,
    )

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "timestamp": expect.Any(int),
            "user_from": None,
            "seen": False,
            "heading": "Your reply was deleted",
            "body": "[Deleted]",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': reply,
            'queue': None,
        },
    ])


def test_self_deleted_reply_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they delete their own reply?"""
    comment = browse.comment.create(
        basic_server_setup['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    reply = browse.reply.create(
        basic_server_setup['token'],
        comment,
        'This is a reply',
    )['reply_id']

    browse.reply.delete(  # type: ignore
        basic_server_setup['token'],
        reply,
    )

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []
