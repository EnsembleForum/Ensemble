"""
# Tests / Integration / Notifications / Reported test

Tests for notifications that a post was reported

* Mods all get notification
* Admin who makes report doesn't get notified
* Mod whose post is reported doesn't get notified
"""
import jestspectation as expect
from ensemble_request import notifications, browse
from ..conftest import ISimpleUsers, IBasicServerSetup, IMakePosts, IAllUsers


def test_mod_notified(
    all_users: IAllUsers,
    make_posts: IMakePosts,
):
    """Do all mods get a notification if a post is reported"""
    browse.post.report(
        all_users['users'][0]['token'],
        make_posts['post1_id'],
    )
    expected = expect.Equals([{
        "notification_id": expect.Any(int),
        "timestamp": expect.Any(int),
        "seen": False,
        "user_from": None,
        "heading": "Post reported",
        "body": make_posts['head1'],
        "post": make_posts['post1_id'],
        "comment": None,
        "reply": None,
        "queue": None,
    }])
    # Mods got notified
    notifs = notifications.list(all_users['mods'][0]['token'])['notifications']
    assert notifs == expected
    notifs = notifications.list(all_users['mods'][1]['token'])['notifications']
    assert notifs == expected
    # Admins got notified
    notifs = notifications.list(
        all_users['admins'][1]['token'])['notifications']
    assert notifs == expected


def test_reporter_not_notified(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """Does the person who submitted the report not get notified?"""
    browse.post.report(basic_server_setup['token'], make_posts['post1_id'])
    assert notifications.list(
        basic_server_setup['token'])['notifications'] == []


def test_reported_op_not_notified(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Does the person whose post got reported not get notified?"""
    browse.post.report(simple_users['user']['token'], make_posts['post1_id'])
    assert notifications.list(
        simple_users['admin']['token'])['notifications'] == []
