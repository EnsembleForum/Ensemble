"""
# Tests / Integration / Notifications / Accepted test

Tests for notifications when answers get accepted

* Commenter gets notification if their comment is accepted by OP
* OP and commenter get notification if a comment on their post is accepted by
  a mod
* OP only gets one notification if their own comment on their post is accepted
  by a mod
* OP doesn't get notification if they accept their own comment
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_commenter_notified_when_accepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do commenters get notified if their comment is accepted by OP?"""
    comment = browse.comment.create(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.comment.accept(
        simple_users['admin']['token'],
        comment,
    )

    mod_notifs = notifications.list(simple_users['mod']['token'])

    assert mod_notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": simple_users['admin']['user_id'],
            "heading": "Answer accepted",
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ])


def test_op_and_commenter_notified_when_accepted_by_mod(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Do commenters and OP get notified if the comment is accepted by a mod?
    """
    comment = browse.comment.create(
        simple_users['user']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.comment.accept(
        simple_users['mod']['token'],
        comment,
    )

    admin_notifs = notifications.list(simple_users['admin']['token'])

    assert admin_notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": simple_users['mod']['user_id'],
            "heading": "Answer accepted on your post",
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
        expect.DictContainingItems({
            "heading": "New comment on your post",
        })
    ])

    user = notifications.list(simple_users['user']['token'])

    assert user['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": simple_users['mod']['user_id'],
            "heading": "Answer accepted",
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ])


def test_op_who_is_commenter_notified_when_accepted_by_mod(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does OP only get notified once if their comment on their own post is
    accepted by a mod?
    """
    comment = browse.comment.create(
        simple_users['admin']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.comment.accept(
        simple_users['mod']['token'],
        comment,
    )

    admin_notifs = notifications.list(simple_users['admin']['token'])

    assert admin_notifs['notifications'] == expect.Equals([
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "user_from": simple_users['mod']['user_id'],
            "heading": "Answer accepted",
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ])


def test_op_no_notif(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Does OP not get notified if they do stuff themselves?"""
    comment = browse.comment.create(
        basic_server_setup['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.comment.accept(
        basic_server_setup['token'],
        comment,
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []
