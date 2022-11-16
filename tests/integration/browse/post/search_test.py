"""
# Tests / Integration / Browse / Post List Searching

Tests for searching with post_list

"""
from ..conftest import ISimpleUsers
from ensemble_request.browse import post_list, post_create


def test_simple(simple_users: ISimpleUsers):
    """
    Search does not return posts whose heading or text do not contain any
    substring of the search term
    """
    token = simple_users["user"]["token"]
    post_id = post_create(token, "First head", "hello there", [])["post_id"]
    post_create(token, "Second head", "good bye", [])

    posts = post_list(token, "hello")["posts"]
    assert len(posts) == 1
    assert posts[0]["post_id"] == post_id


def test_ranking(simple_users: ISimpleUsers):
    """
    Better matches are placed at the top of the returned list
    """
    token = simple_users["user"]["token"]
    post_id1 = post_create(token, "head", "goodbye hello there, sir", [])[
        "post_id"]
    post_id2 = post_create(token, "head", "hello good sir", [])["post_id"]

    posts = post_list(token, "sir the")["posts"]
    assert len(posts) == 2
    assert [p["post_id"] for p in posts] == [post_id1, post_id2]
