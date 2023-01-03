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
    post,
    comment,
)
from backend import consts
from ensemble_request.taskboard import queue_post_list, queue_list
from tests.integration.helpers import get_queue
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
    comment_id = comment.create(mod_token, post_id, "hello")["comment_id"]

    with pytest.raises(http_errors.Forbidden):
        comment.delete(user_token, comment_id)


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
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]

    comment.delete(mod_token, comment_id)
    assert comment.view(user_token, comment_id)["text"] == "[Deleted]"


def test_op_delete(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    OP can delete his own comment
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]

    comment.delete(user_token, comment_id)
    c = comment.view(user_token, comment_id)
    assert c["text"] == "[Deleted]"
    assert c["deleted"]


def test_post_comment_list(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Deleted comment still found in post
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]

    comment.delete(user_token, comment_id)

    assert post.view(user_token, post_id)["comments"] == [comment_id]


def test_edit_deleted_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Cannot edit a deleted comment
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]

    comment.delete(user_token, comment_id)
    with pytest.raises(http_errors.BadRequest):
        comment.edit(user_token, comment_id, "hello")


def test_delete_accepted_comment(
    simple_users: ISimpleUsers
):
    """
    Deleting an accepted comment marks post as unanswered
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    post_id = post.create(user_token, "head", "text", [])["post_id"]
    comment_id = comment.create(user_token, post_id, "hello")["comment_id"]
    comment.accept(user_token, comment_id)

    comment.delete(user_token, comment_id)

    assert not post.view(user_token, post_id)["answered"]

    post_queue_name = post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.MAIN_QUEUE

    queue_id = get_queue(
        queue_list(mod_token)['queues'],
        consts.MAIN_QUEUE
    )["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]
