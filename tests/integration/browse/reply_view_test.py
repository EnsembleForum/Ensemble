"""
# Tests / Integration / Browse / Reply View

Tests for reply view routes

"""
import pytest
from typing import cast
from ..conftest import ISimpleUsers, IMakePosts
from backend.types.identifiers import ReplyId
from backend.util import http_errors
from ensemble_request.browse import (
    add_reply,
    add_comment,
    get_reply,
)


def test_get_reply_success(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """
    Can we get the full details of a valid reply?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    reply_text = "First reply"
    reply_id = add_reply(token, comment_id, reply_text)["reply_id"]

    reply = get_reply(token, reply_id)

    assert reply["text"] == reply_text
    assert isinstance(reply["timestamp"], int)
    assert reply["thanks"] == 0


def test_invalid_reply_id(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """
    If we are given an invalid reply_id, is a 400 error raised?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    reply_id = add_reply(token, comment_id, "reply_text")["reply_id"]

    invalid_reply_id = cast(ReplyId, reply_id + 1)
    with pytest.raises(http_errors.BadRequest):
        get_reply(token, invalid_reply_id)
