"""
# Tests / Integration / Browse / Comment View / Delete

Tests for comment_view/delete
* User cannot delete another person's comment
* OP can delete his own comment
* Mod can delete another person's comment
* Deleted comment's text is replaced
* Deleted comment is still found within the post
* Cannot edit a deleted comment
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    add_comment,
    comment_delete,
    get_comment,
    post_view,
    comment_edit
)
from tests.integration.conftest import ISimpleUsers, IMakePosts


def test_no_permission(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    User cannot delete another user's comment
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(mod_token, post_id, "hello")["comment_id"]

    with pytest.raises(http_errors.Forbidden):
        comment_delete(user_token, comment_id)


def test_mod_delete(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mod can delete another user's comment
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]

    comment_delete(mod_token, comment_id)
    assert get_comment(user_token, comment_id)["text"] == "[Deleted]."


def test_op_delete(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    OP can delete his own comment
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]

    comment_delete(user_token, comment_id)
    comment = get_comment(user_token, comment_id)
    assert comment["text"] == "[Deleted]."
    assert comment["deleted"]


def test_post_comment_list(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Deleted comment still found in post
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]

    comment_delete(user_token, comment_id)

    assert post_view(user_token, post_id)["comments"] == [comment_id]


def test_edit_deleted_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Cannot edit a deleted comment
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(user_token, post_id, "hello")["comment_id"]

    comment_delete(user_token, comment_id)
    with pytest.raises(http_errors.BadRequest):
        comment_edit(user_token, comment_id, "hello")