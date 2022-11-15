"""
# Tests / Integration / Browse / Post anonymous test

Tests for creating and viewing anonymous posts

* Users cannot view OP of anonymous posts
* Mods can view OP of anonymous posts, but still know it's anonymous
* Users can view OP of anonymous posts if OP is them
"""
import jestspectation as expect
from ..conftest import ISimpleUsers
from ensemble_request.browse import post_list, post_create, post_view


def test_post_anon_hidden_users(simple_users: ISimpleUsers):
    post_id = post_create(
        simple_users["mod"]["token"],
        "My anonymous post",
        "I know you are but who am I?",
        tags=[],
        private=False,
        anonymous=True
    )["post_id"]

    # Hidden in post list
    assert post_list(simple_users["user"]["token"])["posts"] == expect.Equals([
        expect.DictContainingItems({
            "post_id": post_id,
            "anonymous": True,
            "author": None,
        })
    ])

    # Hidden in post view
    post = post_view(simple_users["user"]["token"], post_id)
    assert post == expect.DictContainingItems({
        "post_id": post_id,
        "anonymous": True,
        "author": None,
    })


def test_post_anon_shown_mod(simple_users: ISimpleUsers):
    """Mods should be able to view the identity of anonymous users"""
    post_id = post_create(
        simple_users["user"]["token"],
        "My anonymous post",
        "I know you are but who am I?",
        tags=[],
        private=False,
        anonymous=True
    )["post_id"]

    # Shown in post list
    assert post_list(simple_users["mod"]["token"])["posts"] == expect.Equals([
        expect.DictContainingItems({
            "post_id": post_id,
            "anonymous": True,
            "author": simple_users["user"]["user_id"],
        })
    ])

    # Shown in post view
    post = post_view(simple_users["mod"]["token"], post_id)
    assert post == expect.DictContainingItems({
        "post_id": post_id,
        "anonymous": True,
        "author": simple_users["user"]["user_id"],
    })


def test_post_anon_shown_op(simple_users: ISimpleUsers):
    """OP should be able to view their own identity"""
    post_id = post_create(
        simple_users["user"]["token"],
        "My anonymous post",
        "I know you are but who am I?",
        tags=[],
        private=False,
        anonymous=True
    )["post_id"]

    # Shown in post list
    assert post_list(simple_users["user"]["token"])["posts"] == expect.Equals([
        expect.DictContainingItems({
            "post_id": post_id,
            "anonymous": True,
            "author": simple_users["user"]["user_id"],
        })
    ])

    # Shown in post view
    post = post_view(simple_users["user"]["token"], post_id)
    assert post == expect.DictContainingItems({
        "post_id": post_id,
        "anonymous": True,
        "author": simple_users["user"]["user_id"],
    })
