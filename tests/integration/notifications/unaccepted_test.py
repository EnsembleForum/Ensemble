"""
# Tests / Integration / Notifications / Unaccepted test

Tests for notifications when answers get unaccepted

* Commenter gets a notification if their answer is unaccepted
* Commenter doesn't get a notification if they are also person doing action
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_commenter_notified_when_unaccepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do commenters get notified if their uncomment is accepted by OP?"""
    comment = browse.comment.create(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.comment.accept(
        simple_users['mod']['token'],
        comment,
    )

    # Admin unaccepts comment
    browse.comment.accept(
        simple_users['admin']['token'],
        comment,
    )

    mod_notifs = notifications.list(simple_users['mod']['token'])

    assert mod_notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "timestamp": expect.Any(int),
            "seen": False,
            "user_from": simple_users['admin']['user_id'],
            "heading": "Answer unaccepted",
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ]


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

    # Unaccept comment
    browse.comment.accept(
        basic_server_setup['token'],
        comment,
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []
