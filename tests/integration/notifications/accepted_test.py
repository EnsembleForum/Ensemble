"""
# Tests / Integration / Notifications / Accepted test

Tests for notifications when answers get accepted

* Commenter gets notification if their comment is accepted by OP
* OP and commenter get notification if a comment on their post is accepted by
  a mod
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
    comment = browse.add_comment(
        simple_users['mod']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.accept_comment(
        simple_users['admin']['token'],
        comment,
    )

    mod_notifs = notifications.list(simple_users['mod']['token'])

    assert mod_notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": f"Dee accepted your answer for {make_posts['head1']}",
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
    ]

    admin_notifs = notifications.list(simple_users['admin']['token'])

    assert admin_notifs['notifications'] == expect.Equals([
        expect.DictContainingItems({
            "heading": f"Mod commented on your post {make_posts['head1']}",
        }),
    ])


def test_op_commenter_notified_when_accepted_by_mod(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do commenters get notified if their comment is accepted by OP?"""
    comment = browse.add_comment(
        simple_users['user']['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.accept_comment(
        simple_users['mod']['token'],
        comment,
    )

    admin_notifs = notifications.list(simple_users['admin']['token'])

    assert admin_notifs['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": (
                f"Mod accepted an answer on your post {make_posts['head1']}"
            ),
            "body": "This is a comment",
            'post': make_posts['post1_id'],
            'comment': comment,
            'reply': None,
            'queue': None,
        },
        expect.DictContainingItems({
            "heading": f"User commented on your post {make_posts['head1']}",
        })
    ]

    user = notifications.list(simple_users['user']['token'])

    assert user['notifications'] == [
        {
            "notification_id": expect.Any(int),
            "seen": False,
            "heading": (
                f"Mod accepted your answer for {make_posts['head1']}"
            ),
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
    comment = browse.add_comment(
        basic_server_setup['token'],
        make_posts['post1_id'],
        "This is a comment",
    )['comment_id']

    browse.accept_comment(
        basic_server_setup['token'],
        comment,
    )

    notifs = notifications.list(basic_server_setup['token'])

    assert notifs['notifications'] == []
