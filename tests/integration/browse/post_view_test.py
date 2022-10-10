"""
# Tests / Integration / Browse / Post View

Tests for post view routes

"""
import pytest
from typing import cast
from backend.types.identifiers import PostId
from backend.util import http_errors
from tests.integration.conftest import IBasicServerSetup, ITwoPosts
from tests.integration.request.browse import (
    add_reply,
    get_reply,
    post_delete,
    post_list,
    post_view,
    add_comment,
    get_comment,
)


def test_invalid_post_id(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    If we are given an invalid post_id, do we get a 400 error?
    """
    token = basic_server_setup["token"]
    invalid_post_id = (
        max(create_two_posts["post1_id"], create_two_posts["post2_id"]) + 1
    )
    invalid_post_id = cast(PostId, invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        post_view(token, invalid_post_id)


def test_get_post_success(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Can we get the full details of a valid post?
    """
    token = basic_server_setup["token"]
    post = post_view(token, create_two_posts["post1_id"])
    assert post["heading"] == create_two_posts["head1"]
    assert post["text"] == create_two_posts["text1"]
    assert post["comments"] == []
    assert isinstance(post["timestamp"], int)
    assert post["tags"] == []
    assert (
        f"{basic_server_setup['name_first']} {basic_server_setup['name_last']}"
        == post["author"]
    )
    assert post["reacts"]["me_too"] == 0
    assert post["reacts"]["thanks"] == 0


def test_delete_other_user_post(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    TODO: attempt when other users can be registered
    Does deleting another person's post raise a 403 error
    """
    pass


def test_delete_success(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Successful deletion of one of the posts
    """
    token = basic_server_setup["token"]
    del_post_id = post_delete(token, create_two_posts["post1_id"])["post_id"]
    with pytest.raises(http_errors.BadRequest):
        post_view(token, del_post_id)

    posts = post_list(token)
    assert len(posts["posts"]) == 1
    assert posts["posts"][0]["post_id"] == create_two_posts["post2_id"]


def test_empty_text_comment(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Does creating a comment with empty text raise a 400 error?
    """
    token = basic_server_setup["token"]
    with pytest.raises(http_errors.BadRequest):
        add_comment(token, create_two_posts["post1_id"], "")


def test_invalid_post_comment(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    token = basic_server_setup["token"]
    invalid_post_id = (
        max(create_two_posts["post1_id"], create_two_posts["post2_id"]) + 1
    )
    invalid_post_id = cast(PostId, invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        add_comment(token, invalid_post_id, "hello")


def test_add_two_comments(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Add two comments
    List of comment_id returned by post_view should be in order
    of newest to oldest
    """
    token = basic_server_setup["token"]
    post_id = create_two_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token, post_id, "second")["comment_id"]

    post = post_view(token, post_id)
    assert post["comments"] == [comment_id2, comment_id1]


def test_delete_post_deletes_comments(
    basic_server_setup: IBasicServerSetup, create_two_posts: ITwoPosts
):
    """
    Delete a post containing two comments
    The two comments should also be deleted
    """
    token = basic_server_setup["token"]
    post_id = create_two_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token, post_id, "second")["comment_id"]
    reply_id = add_reply(token, comment_id1, "reply_text")["reply_id"]

    post_delete(token, create_two_posts["post1_id"])["post_id"]

    with pytest.raises(http_errors.BadRequest):
        get_comment(token, comment_id1)

    with pytest.raises(http_errors.BadRequest):
        get_comment(token, comment_id2)

    with pytest.raises(http_errors.BadRequest):
        get_reply(token, reply_id)
