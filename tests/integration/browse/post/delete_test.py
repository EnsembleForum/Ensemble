"""
# Tests / Integration / Browse / Post View / Self Delete

Tests for post.view/self_delete

* Fails when non_OP user tries to delete another user's post
* Mods can delete posts they did not create
* OP can see his own deleted post in post.view and post.list
* Mods can see deleted posts in post.view and post.list
* Non-OP users cannot see deleted posts in post.view and post.list
* Deleted posts are sent to the deleted queue
* Cannot edit deleted post
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import post
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
        post.delete(token, make_posts["post1_id"])


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
    post.delete(token, post_id)

    # Deleted post is sent to the deleted queue
    post_queue_name = post.view(token, post_id)["queue"]
    assert post_queue_name == "Deleted"

    queue_id = get_queue(queue_list(token)['queues'],
                         "Deleted")["queue_id"]
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
    post_id = post.create(user_token, "heading", "text", [])["post_id"]
    post.delete(user_token, post_id)

    # Deleted post is sent to the deleted queue
    post_info = post.view(mod_token, post_id)
    post_queue_name = post_info["queue"]
    assert post_queue_name == "Deleted"
    assert post_info["deleted"]
    assert len(post.list(user_token)["posts"]) == 1

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         "Deleted")["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_delete_post_list_permissions(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mods can see deleted posts in post.list
    Non-OP users cannot see deleted posts in post.list
    """
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]

    post.delete(mod_token, make_posts["post1_id"])

    assert len(post.list(mod_token)["posts"]) == 2
    assert len(post.list(user_token)["posts"]) == 1


def test_delete_post_view_permissions(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Mod can view a deleted post from post.view
    User cannot view a deleted post from post.view if he is not OP
    """
    post_id = make_posts["post1_id"]
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]

    post.delete(mod_token, post_id)
    post.view(mod_token, post_id)
    with pytest.raises(http_errors.Forbidden):
        post.view(user_token, post_id)


def test_edit_deleted_post(
    simple_users: ISimpleUsers
):
    """
    Cannot edit deleted post
    """
    user_token = simple_users["user"]["token"]
    post_id = post.create(user_token, "heading", "text", [])["post_id"]
    post.delete(user_token, post_id)
    with pytest.raises(http_errors.BadRequest):
        post.edit(user_token, post_id, "new", "new", [])
