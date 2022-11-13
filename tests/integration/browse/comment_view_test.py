"""
# Tests / Integration / Browse / Comment View

Tests for comment view routes

"""
import pytest
from typing import cast
from backend.types.identifiers import CommentId
from backend.util import http_errors
from ensemble_request.browse import (
    add_reply,
    add_comment,
    get_comment,
)
from tests.integration.conftest import ISimpleUsers, IMakePosts


def test_invalid_comment_id(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    invalid_comment_id = cast(CommentId, comment_id1 + 1)
    with pytest.raises(http_errors.BadRequest):
        get_comment(token, invalid_comment_id)


@pytest.mark.core
def test_get_comment_success(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Can we get the full details of a valid comment?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_text = "first"
    comment_id = add_comment(token, post_id, comment_text)["comment_id"]

    comment = get_comment(token, comment_id)

    assert comment["text"] == comment_text
    assert comment["replies"] == []
    assert isinstance(comment["timestamp"], int)
    assert comment["thanks"] == 0


def test_add_two_replies(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Add two replies to a comment
    List of reply_id returned by post_view should be in order
    of oldest to newest
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    reply_id1 = add_reply(token, comment_id, "first reply")["reply_id"]
    reply_id2 = add_reply(token, comment_id, "second reply")["reply_id"]

    comment = get_comment(token, comment_id)
    assert comment["replies"] == [reply_id1, reply_id2]


def test_empty_text_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does creating a reply with empty text raise a 400 error?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    with pytest.raises(http_errors.BadRequest):
        add_reply(token, comment_id, "")


def test_invalid_comment_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    When trying to reply under a comment whose comment_id does not exist,
    is a 400 error raised?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    invalid_comment_id = cast(CommentId, comment_id+1)
    with pytest.raises(http_errors.BadRequest):
        add_reply(token, invalid_comment_id, "hello")
