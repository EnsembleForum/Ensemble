"""
# Tests / Integration / Browse / Reply View

Tests for reply view routes

"""
import pytest
from typing import cast
from ...conftest import ISimpleUsers, IMakePosts
from backend.types.identifiers import ReplyId, CommentId
from backend.util import http_errors
from ensemble_request.browse import comment, reply


@pytest.mark.core
def test_get_reply_success(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """
    Can we get the full details of a valid reply?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token, post_id, "first")["comment_id"]
    reply_text = "First reply"
    reply_id = reply.create(token, comment_id, reply_text)["reply_id"]

    r = reply.view(token, reply_id)

    assert r["text"] == reply_text
    assert isinstance(r["timestamp"], int)
    assert r["thanks"] == 0


def test_invalid_reply_id(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """
    If we are given an invalid reply_id, is a 400 error raised?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token, post_id, "first")["comment_id"]
    reply_id = reply.create(token, comment_id, "reply_text")["reply_id"]

    invalid_reply_id = cast(ReplyId, reply_id + 1)
    with pytest.raises(http_errors.BadRequest):
        reply.view(token, invalid_reply_id)


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
    comment_id = comment.create(token, post_id, "first")["comment_id"]
    reply_id1 = reply.create(token, comment_id, "first reply")["reply_id"]
    reply_id2 = reply.create(token, comment_id, "second reply")["reply_id"]

    c = comment.view(token, comment_id)
    assert c["replies"] == [reply_id1, reply_id2]


def test_empty_text_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does creating a reply with empty text raise a 400 error?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token, post_id, "first")["comment_id"]
    with pytest.raises(http_errors.BadRequest):
        reply.create(token, comment_id, "")


def test_invalid_comment_reply(simple_users: ISimpleUsers):
    """
    When trying to reply under a comment whose comment_id does not exist,
    is a 400 error raised?
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.BadRequest):
        reply.create(token, CommentId(-1), "hello")
