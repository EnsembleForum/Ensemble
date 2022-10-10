"""
# Tests / Integration / Browse / Comment View

Tests for comment view routes

"""
import pytest
from typing import cast
from backend.types.identifiers import CommentId
from backend.util import http_errors
from tests.integration.conftest import IBasicServerSetup, ITwoPosts
from tests.integration.request.browse import (
    add_reply,
    add_comment,
    get_comment,
)


def test_invalid_comment_id(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = basic_server_setup["token"]
    post_id = create_two_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    invalid_comment_id = cast(CommentId, comment_id1 + 1)
    with pytest.raises(http_errors.BadRequest):
        get_comment(token, invalid_comment_id)


def test_get_comment_success(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Can we get the full details of a valid comment?
    """
    token = basic_server_setup["token"]
    post_id = create_two_posts["post1_id"]
    comment_text = "first"
    comment_id = add_comment(token, post_id, comment_text)["comment_id"]

    comment = get_comment(token, comment_id)

    assert comment["text"] == comment_text
    assert comment["replies"] == []
    assert isinstance(comment["timestamp"], int)
    assert (
        f"{basic_server_setup['name_first']} {basic_server_setup['name_last']}"
        == comment["author"]
    )
    assert comment["reacts"]["me_too"] == 0
    assert comment["reacts"]["thanks"] == 0


def test_add_two_replies(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Add two replies to a comment
    List of reply_id returned by post_view should be in order
    of oldest to newest
    """
    token = basic_server_setup["token"]
    post_id = create_two_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    reply_id1 = add_reply(token, comment_id, "first reply")["reply_id"]
    reply_id2 = add_reply(token, comment_id, "second reply")["reply_id"]

    comment = get_comment(token, comment_id)
    assert comment["replies"] == [reply_id1, reply_id2]


def test_empty_text_reply(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Does creating a reply with empty text raise a 400 error?
    """
    token = basic_server_setup["token"]
    post_id = create_two_posts["post1_id"]
    comment_id = add_comment(token, post_id, "first")["comment_id"]
    with pytest.raises(http_errors.BadRequest):
        add_reply(token, comment_id, "")
