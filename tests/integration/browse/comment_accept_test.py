"""
# Tests / Integration / Browse / Comment View / Accept

Tests for comment_view/accept
* Can the post author, mods and admins mark and unmark a comment as accepted
* Fails when another user besides the post author, mod or admin tries to mark
    a comment as accepted
* Tests for browse/post_view and browse/post_list showing the post as answered
    when the post has at least one comment marked as accepted
* Tests for post being sent to answered queue when it is marked as answered
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    add_comment,
    get_comment,
    post_view,
    accept_comment,
    post_create,
    post_list,
    comment_react
)
from ensemble_request.taskboard import queue_post_list
from tests.integration.conftest import IAllUsers, ISimpleUsers, IMakePosts


def test_get_marking_accepted(
    all_users: IAllUsers,
):
    """
    Can the post author, admins and mods a comment as accepted?
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]
    admin_token = all_users["admins"][0]["token"]
    mod_token = all_users["mods"][0]["token"]

    post_id = post_create(user_token1, "head", "text", [])["post_id"]
    comment_text = "first"
    comment_id = add_comment(user_token2, post_id, comment_text)["comment_id"]

    post = post_view(user_token1, post_id)
    comment = get_comment(user_token1, comment_id)

    # Post author can mark comment as accepted
    assert not post["answered"]
    assert not comment["accepted"]
    assert accept_comment(user_token1, comment_id)["accepted"]
    post = post_view(user_token1, post_id)
    comment = get_comment(user_token1, comment_id)
    assert post["answered"]
    assert comment["accepted"]

    # Admin can mark comment as accepted
    assert not accept_comment(admin_token, comment_id)["accepted"]
    post = post_view(admin_token, post_id)
    comment = get_comment(admin_token, comment_id)
    assert not post["answered"]
    assert not comment["accepted"]
    accept_comment(admin_token, comment_id)
    post = post_view(admin_token, post_id)
    comment = get_comment(admin_token, comment_id)
    assert post["answered"]
    assert comment["accepted"]

    # Mod can mark comment as accepted
    accept_comment(mod_token, comment_id)
    post = post_view(mod_token, post_id)
    comment = get_comment(mod_token, comment_id)
    assert not post["answered"]
    assert not comment["accepted"]
    accept_comment(mod_token, comment_id)
    post = post_view(mod_token, post_id)
    comment = get_comment(mod_token, comment_id)
    assert post["answered"]
    assert comment["accepted"]

    with pytest.raises(http_errors.Forbidden):
        accept_comment(user_token2, comment_id)


def test_get_post_list_answered(
    all_users: IAllUsers,
):
    """
    Do posts returned by post_list show that they are answered correctly?
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]

    post_id = post_create(user_token1, "head", "text", [])["post_id"]
    comment_text = "first"
    comment_id = add_comment(user_token2, post_id, comment_text)["comment_id"]

    posts = post_list(user_token1)
    assert not posts["posts"][0]["answered"]

    accept_comment(user_token1, comment_id)

    posts = post_list(user_token1)
    assert posts["posts"][0]["answered"]


def test_comment_order(
    all_users: IAllUsers,
):
    """
    Are comments sorted by accepted first, then by newest to oldest
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]

    post_id = post_create(user_token1, "head", "text", [])["post_id"]
    comment_id1 = add_comment(user_token2, post_id, "first")["comment_id"]
    comment_id2 = add_comment(user_token2, post_id, "second")["comment_id"]
    comment_id3 = add_comment(user_token2, post_id, "third")["comment_id"]
    comment_id4 = add_comment(user_token2, post_id, "fourth")["comment_id"]

    accept_comment(user_token1, comment_id2)
    accept_comment(user_token1, comment_id4)

    comments = post_view(user_token1, post_id)["comments"]

    assert comments == [comment_id4, comment_id2, comment_id3, comment_id1]


def test_post_view_comments_thanks_order(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Are comments of a post sorted correctly by
    accepted -> thanks -> newest to oldest?
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    token3 = simple_users["admin"]["token"]
    post_id = make_posts["post1_id"]

    comment_id1 = add_comment(token1, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token1, post_id, "second")["comment_id"]
    comment_id3 = add_comment(token1, post_id, "third")["comment_id"]
    comment_id4 = add_comment(token1, post_id, "fourth")["comment_id"]
    comment_id5 = add_comment(token1, post_id, "fifth")["comment_id"]

    # Comment 3 is accepted and has 2 thanks
    comment_react(token1, comment_id3)
    comment_react(token2, comment_id3)
    accept_comment(token3, comment_id3)

    # Comment 1 is accepted and has 1 thanks
    comment_react(token2, comment_id1)
    accept_comment(token3, comment_id1)

    # Comment 2 has 3 thanks
    comment_react(token1, comment_id2)
    comment_react(token3, comment_id2)
    comment_react(token2, comment_id2)

    comments = post_view(token1, post_id)["comments"]
    correct_order = [comment_id3, comment_id1,
                     comment_id2, comment_id5, comment_id4]

    assert comments == correct_order


def test_answered_queue(
    simple_users: ISimpleUsers
):
    """
    Does marking a comment as accepted send the post to the answered queue?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post_create(user_token, "head", "text", [])["post_id"]
    post1_queue = post_view(user_token, post_id)["queue"]
    queue = queue_post_list(mod_token, post1_queue)
    assert queue["queue_name"] == "Main queue"

    comment_id = add_comment(mod_token, post_id, "first")["comment_id"]
    accept_comment(user_token, comment_id)

    post2_queue = post_view(user_token, post_id)["queue"]

    queue = queue_post_list(mod_token, post2_queue)
    assert queue["queue_name"] == "Answered queue"
    assert post_id in queue["posts"]
