"""
# Tests / Integration / Browse / Reply View

Tests for reply view routes

"""
import pytest
from typing import cast
from backend.types.identifiers import ReplyId
from backend.util import http_errors
from tests.integration.request.browse import (
    add_reply,
    add_comment,
    get_reply,
)


def test_get_reply_success(all_users, make_posts):
    """
    Can we get the full details of a valid reply?
    """
    token = all_users["users"][0]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    reply_text = "First reply"
    reply_id = add_reply(token, comment_id, reply_text)["reply_id"]

    reply = get_reply(token, reply_id)

    assert reply["text"] == reply_text
    assert isinstance(reply["timestamp"], int)
    assert reply["reacts"]["me_too"] == 0
    assert reply["reacts"]["thanks"] == 0


def test_invalid_reply_id(all_users, make_posts):
    """
    If we are given an invalid reply_id, is a 400 error raised?
    """
    token = all_users["users"][0]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    reply_id = add_reply(token, comment_id, "reply_text")["reply_id"]

    invalid_reply_id = cast(ReplyId, reply_id + 1)
    with pytest.raises(http_errors.BadRequest):
        get_reply(token, invalid_reply_id)
