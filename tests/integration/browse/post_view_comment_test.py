"""
# Tests / Integration / Browse / Post View / Comment

Tests for post_view/comment

* Fails with empty comment string
* Fails when post trying to comment on does not exist
* Succeeds with valid inputs

"""
import pytest
from typing import cast
from backend.types.identifiers import PostId
from backend.util import http_errors
from tests.integration.request.browse import (
    post_view,
    add_comment,
)


def test_empty_text_comment(all_users, make_posts):
    """
    Does creating a comment with empty text raise a 400 error?
    """
    token = all_users["users"][0]["token"]
    with pytest.raises(http_errors.BadRequest):
        add_comment(token, make_posts["post1_id"], "")


def test_invalid_post_comment(all_users, make_posts):
    token = all_users["users"][0]["token"]
    invalid_post_id = (
        max(make_posts["post1_id"], make_posts["post2_id"]) + 1
    )
    invalid_post_id = cast(PostId, invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        add_comment(token, invalid_post_id, "hello")


def test_add_two_comments(all_users, make_posts):
    """
    Add two comments
    List of comment_id returned by post_view should be in order
    of newest to oldest
    """
    token = all_users["users"][0]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token, post_id, "second")["comment_id"]

    post = post_view(token, post_id)
    assert post["comments"] == [comment_id2, comment_id1]
