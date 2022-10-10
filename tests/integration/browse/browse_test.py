"""
# Tests / Integration / Browse 

Tests for browse routes

"""
import pytest
from backend.util import http_errors
from tests.integration.conftest import IBasicServerSetup
from tests.integration.request.browse import post_list, post_create


def test_empty_post_list(basic_server_setup: IBasicServerSetup):
    """
    Do we get an empty list when there are no posts in the forum?
    """
    token = basic_server_setup["token"]
    posts = post_list(token)
    assert len(posts["posts"]) == 0


def test_create_one_post(basic_server_setup: IBasicServerSetup):
    """
    Can we create a post and get it successfully?
    """
    token = basic_server_setup["token"]
    heading = "First heading"
    text = "First text"
    tags: list[int] = []
    post1_id = post_create(token, heading, text, tags)["post_id"]
    posts = post_list(token)

    assert len(posts["posts"]) == 1

    post1 = posts["posts"][0]
    assert post1_id == post1["post_id"]
    assert (
        f"{basic_server_setup['name_first']} {basic_server_setup['name_last']}"
        == post1["author"]
    )
    assert heading == post1["heading"]
    assert tags == post1["tags"]
    assert post1["reacts"]["me_too"] == 0
    assert post1["reacts"]["thanks"] == 0


def test_create_multiple_posts(basic_server_setup: IBasicServerSetup):
    """
    Can we create multiple posts and get them successfully?
    """
    token = basic_server_setup["token"]
    post1_id = post_create(token, "First heading", "First text", [])["post_id"]
    post2_id = post_create(token, "Second heading", "Second text", [])["post_id"]

    posts = post_list(token)["posts"]

    assert [post2_id, post1_id] == [p["post_id"] for p in posts]
