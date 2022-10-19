"""
# Tests / Integration / Browse / Post View / Edit

Tests for post_view/edit

* Fails when trying to edit another user's post
* Fails when no new heading is provided
    (Should be given old heading if heading should be kept unchanged)
* Fails when no new text is provided
    (Should be given old text if heading should be kept unchanged)
* Succeeds when all inputs are valid
"""
import pytest
from backend.util import http_errors
from tests.integration.request.browse import (
    post_edit,
    post_view,
)


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
