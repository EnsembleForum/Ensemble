"""
# Tests / Integration / Browse / Post View

Tests for post view routes

"""
import pytest
from typing import cast
from backend.types.identifiers import PostId
from backend.util import http_errors
from tests.integration.request.browse import (
    add_reply,
    get_reply,
    post_delete,
    post_edit,
    post_list,
    post_view,
    add_comment,
    get_comment,
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


def test_get_post_success(all_users, make_posts):
    """
    Can we get the full details of a valid post?
    """
    token = all_users["users"][0]["token"]
    post = post_view(token, make_posts["post1_id"])
    assert post["heading"] == make_posts["head1"]
    assert post["text"] == make_posts["text1"]
    assert post["comments"] == []
    assert isinstance(post["timestamp"], int)
    assert post["tags"] == []
    assert post["reacts"]["me_too"] == 0
    assert post["reacts"]["thanks"] == 0


def test_delete_other_user_post(all_users, make_posts):
    """
    Does deleting another person's post raise a 403 error
    """
    token = all_users["users"][1]["token"]
    with pytest.raises(http_errors.Forbidden):
        post_delete(token, make_posts["post1_id"])


def test_delete_success(all_users, make_posts):
    """
    Successful deletion of one of the posts
    """
    token = all_users["users"][0]["token"]
    del_post_id = post_delete(token, make_posts["post1_id"])["post_id"]
    with pytest.raises(http_errors.BadRequest):
        post_view(token, del_post_id)

    posts = post_list(token)
    assert len(posts["posts"]) == 1
    assert posts["posts"][0]["post_id"] == make_posts["post2_id"]


def test_edit_other_user_post(all_users, make_posts):
    """
    Does editing another person's post raise a 403 error
    """
    token = all_users["users"][1]["token"]
    with pytest.raises(http_errors.Forbidden):
        post_edit(token, make_posts["post1_id"], "new head", "new text", [])


def test_edit_no_head(all_users, make_posts):
    """
    Does editing a post raise a 400 error when head or text is empty?
    """
    token = all_users["users"][0]["token"]
    with pytest.raises(http_errors.BadRequest):
        post_edit(token, make_posts["post1_id"], "", "new text", [])
    with pytest.raises(http_errors.BadRequest):
        post_edit(token, make_posts["post1_id"], "new head", "", [])


def test_edit_success(all_users, make_posts):
    """
    Successful edit of one of the posts
    """
    token = all_users["users"][0]["token"]
    new_head = "new_head"
    new_text = "new_text"
    post_id = post_edit(token, make_posts["post1_id"], new_head, new_text, [])[
        "post_id"]

    post = post_view(token, post_id)
    assert post["heading"] == new_head
    assert post["text"] == new_text


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


def test_delete_post_deletes_comments(all_users, make_posts):
    """
    Delete a post containing two comments
    The two comments should also be deleted
    """
    token = all_users["users"][0]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token, post_id, "second")["comment_id"]
    reply_id = add_reply(token, comment_id1, "reply_text")["reply_id"]

    post_delete(token, make_posts["post1_id"])["post_id"]

    with pytest.raises(http_errors.BadRequest):
        get_comment(token, comment_id1)

    with pytest.raises(http_errors.BadRequest):
        get_comment(token, comment_id2)

    with pytest.raises(http_errors.BadRequest):
        get_reply(token, reply_id)
