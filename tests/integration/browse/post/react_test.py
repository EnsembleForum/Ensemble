"""
# Tests / Integration / Browse / Post View / React

Tests for post_view/react

* Succeeds when one user tries to react to a post
* Succeeds when multiple users react & unreact to a post
* User can react to more than one post
* The person viewing the post can see if he has reacted to the post
* Fails when the given post_id does not exist
"""
import pytest
from backend.util import http_errors
from backend.types.identifiers import PostId
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts,
)
from ensemble_request.browse import post


@pytest.mark.core
def test_react_one_user(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Successful reaction by one user
    """
    token = simple_users["user"]["token"]
    token1 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]

    p = post.view(token, post_id)
    assert p["me_too"] == 0

    assert post.react(token, post_id)["user_reacted"]

    p = post.view(token, post_id)
    assert p["me_too"] == 1
    assert p["user_reacted"]

    p = post.view(token1, post_id)
    assert p["me_too"] == 1
    assert not p["user_reacted"]


def test_react_multiple_users(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Successful reacts and un-reacts by multiple users
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]

    p = post.view(token1, post_id)
    assert p["me_too"] == 0

    assert post.react(token1, post_id)["user_reacted"]
    p = post.view(token1, post_id)
    assert p["me_too"] == 1

    post.react(token2, post_id)
    p = post.view(token1, post_id)
    assert p["me_too"] == 2

    assert not post.react(token1, post_id)["user_reacted"]
    p = post.view(token1, post_id)
    assert p["me_too"] == 1

    post.react(token2, post_id)
    p = post.view(token1, post_id)
    assert p["me_too"] == 0


def test_one_user_multiple_posts(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Can a user react to more than one post?
    """
    token = simple_users["user"]["token"]
    post_id1 = make_posts["post1_id"]
    post_id2 = make_posts["post2_id"]

    p = post.view(token, post_id1)
    assert p["me_too"] == 0
    p = post.view(token, post_id2)
    assert p["me_too"] == 0

    post.react(token, post_id1)
    post.react(token, post_id2)

    p = post.view(token, post_id1)
    assert p["me_too"] == 1

    p = post.view(token, post_id2)
    assert p["me_too"] == 1


def test_invalid_post_id(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """
    If we are given an invalid post_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    invalid_post_id = (
        max(make_posts["post1_id"], make_posts["post2_id"]) + 1
    )
    invalid_post_id = PostId(invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        post.react(token, invalid_post_id)
