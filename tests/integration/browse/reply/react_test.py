"""
# Tests / Integration / Browse / Reply View / React

Tests for reply_view/react

* Succeeds when one user tries to react to a reply
* Succeeds when multiple users react & unreact to a reply
* User can react to more than one reply
* Fails when the given reply_id does not exist
"""
import pytest
from backend.util import http_errors
from backend.types.identifiers import ReplyId
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts,
)
from ensemble_request.browse import comment, reply


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
    reply_id = reply.create(token, comment_id, "helo")["reply_id"]
    r = reply.view(token, reply_id)

    assert r["thanks"] == 0

    assert reply.react(token, reply_id)["user_reacted"]

    r = reply.view(token, reply_id)
    assert r["thanks"] == 1
    assert r["user_reacted"]

    r = reply.view(token1, reply_id)
    assert r["thanks"] == 1
    assert not r["user_reacted"]


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
    reply_id = reply.create(token1, comment_id, "helo")["reply_id"]

    r = reply.view(token1, reply_id)
    r = reply.view(token1, reply_id)
    assert r["thanks"] == 0

    assert reply.react(token1, reply_id)["user_reacted"]
    r = reply.view(token1, reply_id)
    assert r["thanks"] == 1

    reply.react(token2, reply_id)
    r = reply.view(token1, reply_id)
    assert r["thanks"] == 2

    assert not reply.react(token1, reply_id)["user_reacted"]
    r = reply.view(token1, reply_id)
    assert r["thanks"] == 1

    reply.react(token2, reply_id)
    r = reply.view(token1, reply_id)
    assert r["thanks"] == 0


def test_one_user_multiple_replies(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Can a user react to more than one reply?
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token1, post_id, "comment")["comment_id"]
    reply_id1 = reply.create(token1, comment_id, "first")["reply_id"]
    reply_id2 = reply.create(token1, comment_id, "second")["reply_id"]

    r = reply.view(token2, reply_id1)
    assert r["thanks"] == 0
    r = reply.view(token2, reply_id2)
    assert r["thanks"] == 0

    reply.react(token2, reply_id1)
    reply.react(token2, reply_id2)

    r = reply.view(token2, reply_id1)
    assert r["thanks"] == 1

    r = reply.view(token2, reply_id2)
    assert r["thanks"] == 1


def test_invalid_comment_id(simple_users: ISimpleUsers):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    invalid_reply_id = ReplyId(1)
    with pytest.raises(http_errors.BadRequest):
        reply.react(token, invalid_reply_id)
