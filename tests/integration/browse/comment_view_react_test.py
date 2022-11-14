"""
# Tests / Integration / Browse / Comment View / React

Tests for comment_view/react

* Succeeds when one user tries to react to a comment
* Succeeds when multiple users react & unreact to a comment
* User can react to more than one comment
* The person viewing the comment can see if he has reacted to the comment
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
    add_comment,
    post_view
)


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
    comment_id = add_comment(token, post_id, "first")["comment_id"]

    comment = get_comment(token, comment_id)
    assert comment["thanks"] == 0

    assert comment_react(token, comment_id)["user_reacted"]

    comment = get_comment(token, comment_id)
    assert comment["thanks"] == 1
    assert comment["user_reacted"]

    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == 1
    assert not comment["user_reacted"]


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
    comment_id = add_comment(token1, post_id, "first")["comment_id"]

    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == 0

    assert comment_react(token1, comment_id)["user_reacted"]
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == 1

    comment_react(token2, comment_id)
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == 2

    assert not comment_react(token1, comment_id)["user_reacted"]
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == 1

    comment_react(token2, comment_id)
    comment = get_comment(token1, comment_id)
    assert comment["thanks"] == 0


def test_one_user_multiple_comments(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Can a user react to more than one comment?
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = add_comment(token1, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token1, post_id, "second")["comment_id"]

    comment = get_comment(token2, comment_id1)
    assert comment["thanks"] == 0
    comment = get_comment(token2, comment_id2)
    assert comment["thanks"] == 0

    comment_react(token2, comment_id1)
    comment_react(token2, comment_id2)

    comment = get_comment(token2, comment_id1)
    assert comment["thanks"] == 1

    comment = get_comment(token2, comment_id2)
    assert comment["thanks"] == 1


def test_post_view_comments_thanks_order(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Are comments of a post sorted correctly by
    accepted -> thanks -> newest to oldest?
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    token3 = simple_users["admin"]["token"]
    post_id = make_posts["post1_id"]

    comment_ids = [add_comment(token1, post_id, "comment")["comment_id"]
                   for i in range(4)]

    # Comment 2 has 3 thanks
    comment_react(token1, comment_ids[1])
    comment_react(token2, comment_ids[1])
    comment_react(token3, comment_ids[1])

    # Comment 4 has 2 thanks
    comment_react(token1, comment_ids[3])
    comment_react(token2, comment_ids[3])

    comments = post_view(token1, post_id)["comments"]
    correct_order = [comment_ids[1], comment_ids[3],
                     comment_ids[2], comment_ids[0]]

    assert comments == correct_order


def test_invalid_comment_id(simple_users: ISimpleUsers):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    invalid_comment_id = CommentId(1)
    with pytest.raises(http_errors.BadRequest):
        comment_react(token, invalid_comment_id)
