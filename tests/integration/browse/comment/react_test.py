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
    comment,
    post
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
    comment_id = comment.create(token, post_id, "first")["comment_id"]

    c = comment.view(token, comment_id)
    assert c["thanks"] == 0

    assert comment.react(token, comment_id)["user_reacted"]

    c = comment.view(token, comment_id)
    assert c["thanks"] == 1
    assert c["user_reacted"]

    c = comment.view(token1, comment_id)
    assert c["thanks"] == 1
    assert not c["user_reacted"]


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
    comment_id = comment.create(token1, post_id, "first")["comment_id"]

    c = comment.view(token1, comment_id)
    assert c["thanks"] == 0

    assert comment.react(token1, comment_id)["user_reacted"]
    c = comment.view(token1, comment_id)
    assert c["thanks"] == 1

    comment.react(token2, comment_id)
    c["thanks"] == 2

    assert not comment.react(token1, comment_id)["user_reacted"]
    c = comment.view(token1, comment_id)
    assert c["thanks"] == 1

    comment.react(token2, comment_id)
    c = comment.view(token1, comment_id)
    assert c["thanks"] == 0


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
    comment_id1 = comment.create(token1, post_id, "first")["comment_id"]
    comment_id2 = comment.create(token1, post_id, "second")["comment_id"]

    c = comment.view(token2, comment_id1)
    assert c["thanks"] == 0
    c = comment.view(token2, comment_id2)
    assert c["thanks"] == 0

    comment.react(token2, comment_id1)
    comment.react(token2, comment_id2)

    c = comment.view(token2, comment_id1)
    assert c["thanks"] == 1

    c = comment.view(token2, comment_id2)
    assert c["thanks"] == 1


def test_post_view_comments_thanks_order(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Are comments of a post sorted correctly by
    accepted -> thanks -> oldest to newest?
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    token3 = simple_users["admin"]["token"]
    post_id = make_posts["post1_id"]

    comment_ids = [comment.create(token1, post_id, "comment")["comment_id"]
                   for i in range(4)]

    # Comment 2 has 3 thanks
    comment.react(token1, comment_ids[1])
    comment.react(token2, comment_ids[1])
    comment.react(token3, comment_ids[1])

    # Comment 4 has 2 thanks
    comment.react(token1, comment_ids[3])
    comment.react(token2, comment_ids[3])

    comments = post.view(token1, post_id)["comments"]
    correct_order = [comment_ids[1], comment_ids[3],
                     comment_ids[0], comment_ids[2]]

    assert comments == correct_order


def test_invalid_comment_id(simple_users: ISimpleUsers):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    invalid_comment_id = CommentId(1)
    with pytest.raises(http_errors.BadRequest):
        comment.react(token, invalid_comment_id)
