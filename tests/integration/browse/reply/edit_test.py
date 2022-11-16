"""
# Tests / Integration / Browse / Comment View / Edit

Tests for comment_view/edit

* Fails when trying to edit another user's reply
* Fails when no new text is provided
    (Should be given old text if heading should be kept unchanged)
* Succeeds when all inputs are valid
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import comment, reply
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
    Does editing another person's reply raise a 403 error
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token1, post_id, "first")["comment_id"]
    reply_id = reply.create(token1, comment_id, "helo")["reply_id"]

    with pytest.raises(http_errors.Forbidden):
        reply.edit(token2, reply_id, "new reply")


def test_edit_empty_params(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Does editing a reply raise a 400 error when text is empty?
    """
    token = basic_server_setup["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token, post_id, "first")["comment_id"]
    reply_id = reply.create(token, comment_id, "helo")["reply_id"]
    with pytest.raises(http_errors.BadRequest):
        reply.edit(token, reply_id, "")


@pytest.mark.core
def test_edit_success(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Successful edit of one of the replies
    """
    token = basic_server_setup["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(token, post_id, "first")["comment_id"]
    old_reply = "hello"
    reply_id = reply.create(token, comment_id, old_reply)["reply_id"]
    new_reply = "new reply"

    assert reply.view(token, reply_id)["text"] == old_reply

    reply.edit(token, reply_id, new_reply)

    assert reply.view(token, reply_id)["text"] == new_reply
