"""
# Tests / Integration / Browse / Post View / Close

Tests for post.view/close

* Fails when no permission to close post
* Fails when no permission to view closed post
* Post_list correctly shows that a post is closed
* Post_view correctly shows that a post is closed
* OP can view his own closed post
* Mods and admins can view closed posts
* Closing a post sends it to the closed queue,
    un-closing sends it back to main queue
"""
import pytest
from resources import consts
from backend.util import http_errors
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts,
    IAllUsers,
)
from ensemble_request.browse import post, comment
from ensemble_request.taskboard import queue_post_list, queue_list
from tests.integration.helpers import get_queue


def test_no_permission_to_close(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Fails when user with no permission tries to close post
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    with pytest.raises(http_errors.Forbidden):
        post.close(user_token, post_id)


def test_no_permission_to_view(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Fails when user with no permission tries to view a closed post
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    post.close(mod_token, post_id)
    with pytest.raises(http_errors.Forbidden):
        post.view(user_token, post_id)


@pytest.mark.core
def test_closed_post_view(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Does post.view correctly show whether the post is closed or not?
    """
    mod_token = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]

    p = post.view(mod_token, post_id)
    assert not p["closed"]

    post.close(mod_token, post_id)
    p = post.view(mod_token, post_id)
    assert p["closed"]


def test_closed_post_list(
    simple_users: ISimpleUsers,
):
    """
    Does post.list correctly show whether the post is closed or not?
    """
    mod_token = simple_users["mod"]["token"]
    post_id = post.create(mod_token, "head", "text", [])["post_id"]

    p = post.list(mod_token)["posts"][0]
    assert not p["closed"]

    post.close(mod_token, post_id)
    p = post.list(mod_token)["posts"][0]
    assert p["closed"]


def test_diff_users_closed_post_list(all_users: IAllUsers):
    """
    Can users with permissions to view closed posts
    view closed posts in post.list?
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]
    mod_token = all_users["mods"][0]["token"]
    admin_token = all_users["admins"][0]["token"]

    # User 1 creates a public post
    heading = "First heading"
    text = "First text"
    tags: list[int] = []
    post_id1 = post.create(user_token1, heading, text, tags)["post_id"]

    # User 2 creates a public post
    heading = "Second heading"
    text = "Second text"
    post_id2 = post.create(user_token2, heading, text, tags)["post_id"]

    # User 1's post is closed
    post.close(mod_token, post_id1)

    # User 1 can view both posts
    posts = post.list(user_token1)["posts"]
    assert len(posts) == 2
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id1, post_id2])

    # User 2 cannot view User 1's post
    posts = post.list(user_token2)["posts"]
    assert len(posts) == 1
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id2])

    # Admin can view both posts
    posts = post.list(admin_token)["posts"]
    assert len(posts) == 2
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id1, post_id2])

    # Mod can view both posts
    posts = post.list(mod_token)["posts"]
    assert len(posts) == 2
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id1, post_id2])


def test_closed_queue(
    simple_users: ISimpleUsers
):
    """
    Does closing a post send it to the closed queue?
    Does un-closing a post send it to the main queue?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post.create(user_token, "head", "text", [])["post_id"]

    # Closing a post sends it to the closed queue
    post.close(mod_token, post_id)
    post_queue_name = post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.CLOSED_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.CLOSED_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]

    # Un-closing a post sends it back to the main queue
    post.close(mod_token, post_id)
    post_queue_name = post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.MAIN_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.MAIN_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_edit_unpost_close(
    simple_users: ISimpleUsers
):
    """
    If OP edits the closed post, his post is sent back to the main queue
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post.create(user_token, "head", "text", [])["post_id"]

    # Closing a post sends it to the closed queue
    post.close(mod_token, post_id)

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.CLOSED_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]

    # OP editing the post sends it back to the main queue
    post.edit(user_token, post_id, "hi", "there", [])

    post_queue_name = post.view(user_token, post_id)["queue"]
    assert post_queue_name == "Main"

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.MAIN_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_close_answered_post(
    simple_users: ISimpleUsers
):
    """
    Does un-closing an answered post send it to the answered queue?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post.create(user_token, "head", "text", [])["post_id"]
    comment_id = comment.create(user_token, post_id, "first")["comment_id"]
    comment.accept(user_token, comment_id)

    # Closing a post sends it to the closed queue
    post.close(mod_token, post_id)

    # Un-closing a post sends it back to the answered queue
    post.close(mod_token, post_id)
    post_queue_name = post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.ANSWERED_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.ANSWERED_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_edit_answered_closed_post(
    simple_users: ISimpleUsers
):
    """
    If OP edits the closed post that is answered,
    his post is sent back to the answered queue
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post.create(user_token, "head", "text", [])["post_id"]
    comment_id = comment.create(user_token, post_id, "first")["comment_id"]
    comment.accept(user_token, comment_id)

    # OP editing the post sends it back to the answered queue
    post.edit(user_token, post_id, "hi", "there", [])

    post_queue_name = post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.ANSWERED_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.ANSWERED_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]
