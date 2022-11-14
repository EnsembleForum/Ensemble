"""
# Tests / Integration / Browse / Post View / Self Delete

Tests for post_view/self_delete

* Fails when non_OP user tries to delete another user's post
* Mods can delete posts they did not create
* OP can see his own deleted post in post_view and post_list
* Mods can see deleted posts in post_view and post_list
* Non-OP users cannot see deleted posts in post_view and post_list
* Deleted posts are sent to the deleted queue
* Cannot edit deleted post
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    post_delete,
    post_list,
    post_view,
    post_create,
    post_edit
)
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts,
)
from ensemble_request.taskboard import (
    queue_post_list,
    queue_list,
)

from tests.integration.helpers import get_queue


def test_no_permission(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does deleting another person's post raise a 403 error
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.Forbidden):
        post_delete(token, make_posts["post1_id"])


@pytest.mark.core
def test_mod_delete_other_user_post(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mod can delete another person's post
    """
    post_id = make_posts["post1_id"]
    token = simple_users["mod"]["token"]
    post_delete(token, post_id)

    # Deleted post is sent to the deleted queue
    post_queue_name = post_view(token, post_id)["queue"]
    assert post_queue_name == "Deleted queue"

    queue_id = get_queue(queue_list(token)['queues'],
                         "Deleted queue")["queue_id"]
    queue = queue_post_list(token, queue_id)
    assert post_id in queue["posts"]


def test_OP_delete(
    simple_users: ISimpleUsers
):
    """
    Successful deletion of one of the posts by the OP
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]
    heading = "head"
    post_id = post_create(user_token, heading, "text", [])["post_id"]
    post_delete(user_token, post_id)

    # Deleted post is sent to the deleted queue
    post_info = post_view(mod_token, post_id)
    post_queue_name = post_info["queue"]
    assert post_queue_name == "Deleted queue"
    assert post_info["deleted"]
    assert post_info["heading"] == f"[Deleted] {heading}"
    assert len(post_list(user_token)["posts"]) == 1

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         "Deleted queue")["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_delete_post_list_permissions(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mods can see deleted posts in post_list
    Non-OP users cannot see deleted posts in post_list
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]

    post_delete(mod_token, make_posts["post1_id"])

    assert len(post_list(mod_token)["posts"]) == 2
    assert len(post_list(user_token)["posts"]) == 1


def test_delete_post_view_permissions(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mod can view a deleted post from post_view
    User cannot view a deleted post from post_view if he is not OP
    """
    post_id = make_posts["post1_id"]
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]

    post_delete(mod_token, post_id)
    post_view(mod_token, post_id)
    with pytest.raises(http_errors.Forbidden):
        post_view(user_token, post_id)


def test_edit_deleted_post(
    simple_users: ISimpleUsers
):
    """
    Cannot edit deleted post
    """
    user_token = simple_users["user"]["token"]
    post_id = post_create(user_token, "heading", "text", [])["post_id"]
    post_delete(user_token, post_id)
    with pytest.raises(http_errors.BadRequest):
        post_edit(user_token, post_id, "new", "new", [])
