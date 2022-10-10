"""
# Tests / Integration / Browse

Tests for browse routes

"""
import pytest
from backend.util import http_errors
from tests.integration.request.browse import post_list, post_create


def test_empty_post_list(all_users):
    """
    Do we get an empty list when there are no posts in the forum?
    """
    token = all_users["users"][0]["token"]
    posts = post_list(token)
    assert len(posts["posts"]) == 0


def test_create_one_post(all_users):
    """
    Can we create a post and get it successfully?
    """
    token = all_users["users"][0]["token"]
    heading = "First heading"
    text = "First text"
    tags: list[int] = []
    post1_id = post_create(token, heading, text, tags)["post_id"]
    posts = post_list(token)

    assert len(posts["posts"]) == 1

    post1 = posts["posts"][0]
    assert post1_id == post1["post_id"]
    assert heading == post1["heading"]
    assert tags == post1["tags"]
    assert post1["reacts"]["me_too"] == 0
    assert post1["reacts"]["thanks"] == 0


def test_create_multiple_posts(all_users):
    """
    Can we create multiple posts and get them successfully?
    """
    token = all_users["users"][0]["token"]
    post1_id = post_create(token, "First head", "First text", [])["post_id"]
    post2_id = post_create(token, "Second head", "Second text", [])["post_id"]

    posts = post_list(token)["posts"]

    assert [post2_id, post1_id] == [p["post_id"] for p in posts]


def test_empty_heading_text(all_users):
    """
    If we try to create a post without a heading or text, do we get a
    400 error?
    """
    token = all_users["users"][0]["token"]
    with pytest.raises(http_errors.BadRequest):
        post_create(token, "", "First text", [])

    with pytest.raises(http_errors.BadRequest):
        post_create(token, "First heading", "", [])
