"""
# Tests / Integration / Browse / Reply View / Delete

Tests for reply_view/delete
* User cannot delete another person's reply
* OP can delete his own reply
* Mod can delete another person's reply
* Deleted reply's text is replaced
* Deleted reply is still found within the post
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    add_comment,
    get_comment,
    get_reply,
    add_reply,
    reply_delete,
    reply_edit
)
from tests.integration.conftest import ISimpleUsers, IMakePosts


def test_no_permission(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    User cannot delete another user's reply
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(mod_token, post_id, "hello")["comment_id"]
    reply_id = add_reply(mod_token, comment_id, "reply")["reply_id"]

    with pytest.raises(http_errors.Forbidden):
        reply_delete(user_token, reply_id)


def test_mod_delete(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mod can delete another user's reply
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]
    reply_id = add_reply(user_token, comment_id, "reply")["reply_id"]

    reply_delete(mod_token, reply_id)
    assert get_reply(user_token, reply_id)["text"] == "[Deleted]."


def test_op_delete(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    OP can delete his own reply
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]
    reply_id = add_reply(user_token, comment_id, "reply")["reply_id"]

    reply_delete(user_token, reply_id)
    reply = get_reply(user_token, reply_id)
    assert reply["text"] == "[Deleted]."
    assert reply["deleted"]


def test_post_comment_list(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Deleted reply still found in comment
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]
    reply_id = add_reply(user_token, comment_id, "reply")["reply_id"]

    reply_delete(user_token, reply_id)

    assert get_comment(user_token, comment_id)["replies"] == [reply_id]


def test_edit_deleted_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    OP can delete his own reply
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]
    reply_id = add_reply(user_token, comment_id, "reply")["reply_id"]

    reply_delete(user_token, reply_id)
    with pytest.raises(http_errors.BadRequest):
        reply_edit(user_token, reply_id, "hello")
