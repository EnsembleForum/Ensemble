"""
# Tests / Integration / Browse / Post View

Tests for post view routes

* Fails with invalid post_id
* Success with valid post_id
"""
import pytest
from datetime import datetime, timedelta
from typing import cast
from ...conftest import ISimpleUsers, IMakePosts
from backend.types.identifiers import PostId
from backend.util import http_errors
from ensemble_request.browse import post


def test_invalid_post_id(simple_users: ISimpleUsers, make_posts: IMakePosts):
    """
    If we are given an invalid post_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    invalid_post_id = (
        max(make_posts["post1_id"], make_posts["post2_id"]) + 1
    )
    invalid_post_id = cast(PostId, invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        post.view(token, invalid_post_id)


@pytest.mark.core
def test_get_post_success(simple_users: ISimpleUsers):
    """
    Can we get the full details of a valid post?
    """
    token = simple_users["user"]["token"]
    heading = "heading"
    text = "text"
    post_time = datetime.now()
    post_id = post.create(token, "heading", "text", [])["post_id"]
    p = post.view(token, post_id)
    assert p["heading"] == heading
    assert p["text"] == text
    assert p["comments"] == []
    assert datetime.fromtimestamp(
        float(p["timestamp"])) - post_time < timedelta(seconds=5)
    assert p["tags"] == []
    assert p["me_too"] == 0
    assert not p["private"]
    assert not p["anonymous"]
