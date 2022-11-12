"""
# Tests / Integration / Notifications / Deleted test

Tests for notifications when deleting posts

* Users get notified when their post is deleted
* User doesn't get notified if they delete their own post
"""
import pytest
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


# Mods don't have permission to delete other user's posts yet
@pytest.mark.xfail
def test_deleted_post_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their posts are deleted?"""
    browse.post_delete(simple_users['mod']['token'], make_posts['post1_id'])

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": f"A moderator deleted your post {make_posts['head1']}",
            "body": "",
            'post': make_posts['post1_id'],
            'comment': None,
            'reply': None,
            'queue': None,
        },
    ]


def test_self_deleted_post_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they delete their own post?"""
    browse.post_delete(basic_server_setup['token'], make_posts['post1_id'])

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []


# No route for deleting comments or replies
@pytest.mark.xfail
def test_deleted_comment_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their comments are deleted?"""
    comment = browse.add_comment(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    browse.comment_delete(  # type: ignore
        simple_users['mod']['token'],
        comment,
    )

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": "A moderator deleted your comment 'This is a comment'",
            "body": "",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ]


# No way to delete comments
@pytest.mark.xfail
def test_self_deleted_comment_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they delete their own comment?"""
    comment = browse.add_comment(
        basic_server_setup['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    browse.comment_delete(  # type: ignore
        basic_server_setup['token'],
        comment,
    )

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []


# No route for deleting replies
@pytest.mark.xfail
def test_deleted_reply_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their replies are deleted?"""
    comment = browse.add_comment(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    reply = browse.add_reply(
        simple_users['admin']['token'],
        comment,
        'This is a reply',
    )['reply_id']

    browse.reply_delete(  # type: ignore
        simple_users['mod']['token'],
        reply,
    )

    notifs = notifications.list(simple_users['admin']['token'])
    assert notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": "A moderator deleted your reply 'This is a reply'",
            "body": "",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': reply,
            'queue': None,
        },
    ]


# No way to delete replies
@pytest.mark.xfail
def test_self_deleted_reply_no_notification(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Do users not get notified if they delete their own reply?"""
    comment = browse.add_comment(
        basic_server_setup['token'],
        make_posts['post1_id'],
        'This is a comment',
    )['comment_id']

    reply = browse.add_reply(
        basic_server_setup['token'],
        comment,
        'This is a reply',
    )['reply_id']

    browse.reply_delete(  # type: ignore
        basic_server_setup['token'],
        reply,
    )

    notifs = notifications.list(basic_server_setup['token'])
    assert notifs['notifications'] == []
