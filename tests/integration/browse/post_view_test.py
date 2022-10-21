"""
# Tests / Integration / Browse / Post View

Tests for post view routes

* Fails with invalid post_id
* Success with valid post_id
"""
import pytest
from datetime import datetime, timedelta
from typing import cast
from backend.types.identifiers import PostId
from backend.util import http_errors
from tests.integration.request.browse import (
    post_create,
    post_view,
)


def test_invalid_post_id(all_users, make_posts):
    """
    If we are given an invalid post_id, do we get a 400 error?
    """
    token = all_users["users"][0]["token"]
    invalid_post_id = (
        max(make_posts["post1_id"], make_posts["post2_id"]) + 1
    )
    invalid_post_id = cast(PostId, invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        post_view(token, invalid_post_id)


def test_get_post_success(all_users):
    """
    Can we get the full details of a valid post?
    """
    token = all_users["users"][0]["token"]
    heading = "heading"
    text = "text"
    post_time = datetime.now()
    post_id = post_create(token, "heading", "text", [])["post_id"]
    post = post_view(token, post_id)
    assert post["heading"] == heading
    assert post["text"] == text
    assert post["comments"] == []
    assert datetime.fromtimestamp(
        float(post["timestamp"])) - post_time < timedelta(seconds=5)
    assert post["tags"] == []
    assert post["thanks"] == 0
