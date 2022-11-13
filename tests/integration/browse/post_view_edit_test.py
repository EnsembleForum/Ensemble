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
from ensemble_request.browse import (
    post_edit,
    post_view,
)
from tests.integration.conftest import (
    IBasicServerSetup,
    ISimpleUsers,
    IMakePosts,
)


def test_edit_other_user_post(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does editing another person's post raise a 403 error
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.Forbidden):
        post_edit(token, make_posts["post1_id"], "new head", "new text", [])


def test_edit_empty_params(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Does editing a post raise a 400 error when head or text is empty?
    """
    token = basic_server_setup["token"]
    with pytest.raises(http_errors.BadRequest):
        post_edit(token, make_posts["post1_id"], "", "new text", [])
    with pytest.raises(http_errors.BadRequest):
        post_edit(token, make_posts["post1_id"], "new head", "", [])


@pytest.mark.core
def test_edit_success(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Successful edit of one of the posts
    """
    token = basic_server_setup["token"]
    new_head = "new_head"
    new_text = "new_text"
    post_edit(token, make_posts["post1_id"], new_head, new_text, [])

    post = post_view(token, make_posts["post1_id"])
    assert post["heading"] == new_head
    assert post["text"] == new_text
