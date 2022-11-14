"""
# Tests / Integration / Browse

Tests for browse routes

* browse/post_list returns an empty list when there are no posts
* browse/post_list returns the correct list containing >= 1 posts
* browse/create succeeds creating a post when inputs are valid
* browse/create fails when heading/text are empty
"""
import pytest
from ..conftest import ISimpleUsers
from backend.util import http_errors
from ensemble_request.browse import post_list, post_create


def test_empty_post_list(simple_users: ISimpleUsers):
    """
    Do we get an empty list when there are no posts in the forum?
    """
    token = simple_users["user"]["token"]
    posts = post_list(token)
    assert len(posts["posts"]) == 0


@pytest.mark.core
def test_create_one_post(simple_users: ISimpleUsers):
    """
    Can we create a post and get it successfully?
    """
    token = simple_users["user"]["token"]
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
    assert post1["me_too"] == 0


def test_create_multiple_posts(simple_users: ISimpleUsers):
    """
    Can we create multiple posts and get them successfully?
    """
    token = simple_users["user"]["token"]
    post1_id = post_create(token, "First head", "First text", [])["post_id"]
    post2_id = post_create(token, "Second head", "Second text", [])["post_id"]

    posts = post_list(token)["posts"]

    assert [post2_id, post1_id] == [p["post_id"] for p in posts]


def test_empty_heading_text(simple_users: ISimpleUsers):
    """
    If we try to create a post without a heading or text, do we get a
    400 error?
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.BadRequest):
        post_create(token, "", "First text", [])

    with pytest.raises(http_errors.BadRequest):
        post_create(token, "First heading", "", [])
