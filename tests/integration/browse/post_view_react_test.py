"""
# Tests / Integration / Browse / Post View / React

Tests for post_view/react

* Succeeds when one user tries to react to a post
* Succeeds when multiple users react & unreact to a post
"""

from ensemble_request.browse import (
    post_react,
    post_view,
)


def test_react_one_user(all_users, make_posts):
    """
    Successful reaction by one user
    """
    token = all_users["users"][0]["token"]
    post_id = make_posts["post1_id"]

    post = post_view(token, post_id)
    assert post["me_too"] == 0

    post_react(token, post_id)

    post = post_view(token, post_id)
    assert post["me_too"] == 1


def test_react_multiple_users(all_users, make_posts):
    """
    Successful reacts and unreacts by multiple users
    """
    token1 = all_users["users"][0]["token"]
    token2 = all_users["users"][1]["token"]
    post_id = make_posts["post1_id"]

    post = post_view(token1, post_id)
    assert post["me_too"] == 0

    post_react(token1, post_id)
    post = post_view(token1, post_id)
    assert post["me_too"] == 1

    post_react(token2, post_id)
    post = post_view(token1, post_id)
    assert post["me_too"] == 2

    post_react(token1, post_id)
    post = post_view(token1, post_id)
    assert post["me_too"] == 1

    post_react(token2, post_id)
    post = post_view(token1, post_id)
    assert post["me_too"] == 0
