"""
# Tests / Integration / Browse / Comment View / Edit

Tests for comment_view/edit

* Fails when trying to edit another user's comment
* Fails when no new text is provided
    (Should be given old text if heading should be kept unchanged)
* Succeeds when all inputs are valid
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    comment_edit,
    get_comment,
    add_comment
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
    Does editing another person's comment raise a 403 error
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token2, post_id, "hello")["comment_id"]
    with pytest.raises(http_errors.Forbidden):
        comment_edit(token1, comment_id, "new comment")


def test_edit_empty_params(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Does editing a comment raise a 400 error when text is empty?
    """
    token = basic_server_setup["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token, post_id, "hello")["comment_id"]
    with pytest.raises(http_errors.BadRequest):
        comment_edit(token, comment_id, "")


@pytest.mark.core
def test_edit_success(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Successful edit of one of the comments
    """
    token = basic_server_setup["token"]
    post_id = make_posts["post1_id"]
    old_comment = "hello"
    comment_id = add_comment(token, post_id, old_comment)["comment_id"]
    new_comment = "new_comment"

    assert get_comment(token, comment_id)["text"] == old_comment

    comment_edit(token, comment_id, new_comment)

    assert get_comment(token, comment_id)["text"] == new_comment
