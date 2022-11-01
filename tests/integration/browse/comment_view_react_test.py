"""
# Tests / Integration / Browse / Comment View / React

Tests for comment_view/react

* Succeeds when one user tries to react to a comment
* Succeeds when multiple users react & unreact to a comment
* User can react to more than one comment
* Fails when the given comment_id does not exist
"""
import pytest
from backend.util import http_errors
from backend.types.identifiers import CommentId
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts,
)
from ensemble_request.browse import (
    comment_react,
    get_comment,
    add_comment
)


def test_react_one_user(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Successful reaction by one user
    """
    token = simple_users["user"]["token"]
    user_id = simple_users["user"]["user_id"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    comment = get_comment(token, comment_id)

    assert comment["thanks"] == []

    comment_react(token, comment_id)

    comment = get_comment(token, comment_id)
    assert comment["thanks"] == [user_id]


def test_react_multiple_users(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Successful reacts and un-reacts by multiple users
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    user_id1 = simple_users["user"]["user_id"]
    user_id2 = simple_users["mod"]["user_id"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token1, post_id, "first")["comment_id"]

    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == []

    comment_react(token1, comment_id)
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == [user_id1]

    comment_react(token2, comment_id)
    comment = get_comment(token1, comment_id)
    assert sorted(comment["thanks"]) == sorted([user_id1, user_id2])

    comment_react(token1, comment_id)
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == [user_id2]

    comment_react(token2, comment_id)
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == []


def test_one_user_multiple_comments(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Can a user react to more than one comment?
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    user_id = simple_users["mod"]["user_id"]
    post_id = make_posts["post1_id"]
    comment_id1 = add_comment(token1, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token1, post_id, "second")["comment_id"]

    comment = get_comment(token2, comment_id1)
    assert comment["thanks"] == []
    comment = get_comment(token2, comment_id2)
    assert comment["thanks"] == []

    comment_react(token2, comment_id1)
    comment_react(token2, comment_id2)

    comment = get_comment(token2, comment_id1)
    assert comment["thanks"] == [user_id]

    comment = get_comment(token2, comment_id2)
    assert comment["thanks"] == [user_id]


def test_invalid_comment_id(simple_users: ISimpleUsers):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    invalid_comment_id = CommentId(1)
    with pytest.raises(http_errors.BadRequest):
        comment_react(token, invalid_comment_id)
