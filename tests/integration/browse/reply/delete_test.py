"""
# Tests / Integration / Browse / Reply View / Delete

Tests for reply_view/delete
* User cannot delete another person's reply
* OP can delete his own reply
* Mod can delete another person's reply
* Deleted reply's text is replaced
* Deleted reply is still found within the post
* Cannot edit a deleted reply
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import comment, reply
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
    comment_id = comment.create(mod_token, post_id, "hello")["comment_id"]
    reply_id = reply.create(mod_token, comment_id, "reply")["reply_id"]

    with pytest.raises(http_errors.Forbidden):
        reply.delete(user_token, reply_id)


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
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]
    reply_id = reply.create(user_token, comment_id, "reply")["reply_id"]

    reply.delete(mod_token, reply_id)
    assert reply.view(user_token, reply_id)["text"] == "[Deleted]"


def test_op_delete(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    OP can delete his own reply
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]
    reply_id = reply.create(user_token, comment_id, "reply")["reply_id"]

    reply.delete(user_token, reply_id)
    r = reply.view(user_token, reply_id)
    assert r["text"] == "[Deleted]"
    assert r["deleted"]


def test_post_comment_list(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Deleted reply still found in comment
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]
    reply_id = reply.create(user_token, comment_id, "reply")["reply_id"]

    reply.delete(user_token, reply_id)

    assert comment.view(user_token, comment_id)["replies"] == [reply_id]


def test_edit_deleted_reply(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Cannot edit a deleted reply
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]
    reply_id = reply.create(user_token, comment_id, "reply")["reply_id"]

    reply.delete(user_token, reply_id)
    with pytest.raises(http_errors.BadRequest):
        reply.edit(user_token, reply_id, "hello")
