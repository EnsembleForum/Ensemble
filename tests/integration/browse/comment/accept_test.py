"""
# Tests / Integration / Browse / Comment View / Accept

Tests for comment_view/accept
* Can the post author, mods and admins mark and unmark a comment as accepted
* Fails when another user besides the post author, mod or admin tries to mark
  a comment as accepted
* Tests for browse/browse.post.view and browse/browse.post.list showing the
  post as answered when the post has at least one comment marked as accepted
* Tests for post being sent to answered queue when it is marked as answered,
  and sent back to the main queue when it is marked as unanswered
"""
import pytest
from backend.util import http_errors
from ensemble_request import browse
from resources import consts
from ensemble_request.taskboard import queue_post_list, queue_list
from tests.integration.helpers import get_queue
from tests.integration.conftest import IAllUsers, ISimpleUsers, IMakePosts


@pytest.mark.core
def test_OP_mark_accepted(simple_users: ISimpleUsers):
    """
    Can the post author mark a comment as accepted?
    """
    token = simple_users["user"]["token"]
    post_id = browse.post.create(token, "head", "text", [])["post_id"]
    comment_id = browse.comment.create(token, post_id, "hello")["comment_id"]

    post = browse.post.view(token, post_id)
    comment = browse.comment.view(token, comment_id)

    # Post author can mark comment as accepted
    assert not post["answered"]
    assert not comment["accepted"]
    assert browse.comment.accept(token, comment_id)["accepted"]
    post = browse.post.view(token, post_id)
    comment = browse.comment.view(token, comment_id)
    assert post["answered"] == comment_id
    assert comment["accepted"]


def test_mod_mark_accepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Can a mod mark a comment he did not write as accepted?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = browse.comment.create(
        user_token, post_id, "hello")["comment_id"]

    post = browse.post.view(mod_token, post_id)
    comment = browse.comment.view(mod_token, comment_id)

    # Mod can mark comment as accepted
    assert not post["answered"]
    assert not comment["accepted"]
    assert browse.comment.accept(mod_token, comment_id)["accepted"]
    post = browse.post.view(mod_token, post_id)
    comment = browse.comment.view(mod_token, comment_id)
    assert post["answered"] == comment_id
    assert comment["accepted"]


def test_get_marking_accepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Is an error raised when non-OP who is not a mod or admin tries to
    mark a comment as accepted?
    """
    user_token = simple_users["user"]["token"]
    admin_token = simple_users["admin"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = browse.comment.create(
        admin_token, post_id, "hello")["comment_id"]

    with pytest.raises(http_errors.Forbidden):
        browse.comment.accept(user_token, comment_id)


def test_only_one_comment_accepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Testing for only one comment accepted per post
    """
    token = simple_users["admin"]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = browse.comment.create(token, post_id, "hello")["comment_id"]
    comment_id2 = browse.comment.create(token, post_id, "hello1")["comment_id"]

    assert not browse.comment.view(token, comment_id1)["accepted"]
    assert not browse.comment.view(token, comment_id2)["accepted"]

    browse.comment.accept(token, comment_id1)
    assert browse.comment.view(token, comment_id1)["accepted"]
    assert not browse.comment.view(token, comment_id2)["accepted"]

    browse.comment.accept(token, comment_id2)
    assert browse.comment.view(token, comment_id2)["accepted"]
    assert not browse.comment.view(token, comment_id1)["accepted"]


def test_get_post_list_answered(
    all_users: IAllUsers,
):
    """
    Do posts returned by browse.post.list show that they are answered
    correctly?
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]

    post_id = browse.post.create(user_token1, "head", "text", [])["post_id"]
    comment_text = "first"
    comment_id = browse.comment.create(
        user_token2, post_id, comment_text)["comment_id"]

    posts = browse.post.list(user_token1)
    assert not posts["posts"][0]["answered"]

    browse.comment.accept(user_token1, comment_id)

    posts = browse.post.list(user_token1)
    assert posts["posts"][0]["answered"]


def test_comment_order(
    all_users: IAllUsers,
):
    """
    Are comments sorted by accepted first, then by newest to oldest
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]

    post_id = browse.post.create(user_token1, "head", "text", [])["post_id"]
    comment_id1 = browse.comment.create(
        user_token2, post_id, "first")["comment_id"]
    comment_id2 = browse.comment.create(
        user_token2, post_id, "second")["comment_id"]
    comment_id3 = browse.comment.create(
        user_token2, post_id, "third")["comment_id"]
    comment_id4 = browse.comment.create(
        user_token2, post_id, "fourth")["comment_id"]

    browse.comment.accept(user_token1, comment_id2)

    comments = browse.post.view(user_token1, post_id)["comments"]

    assert comments == [comment_id2, comment_id4, comment_id3, comment_id1]


def test_post_view_comments_order(
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

    comment_ids = [
        browse.comment.create(token1, post_id, "comment")["comment_id"]
        for i in range(5)
    ]

    # Comment 3 is accepted and has 2 thanks
    browse.comment.react(token1, comment_ids[2])
    browse.comment.react(token2, comment_ids[2])
    browse.comment.accept(token3, comment_ids[2])

    # Comment 1 has 1 thanks
    browse.comment.react(token2, comment_ids[0])

    # Comment 2 has 3 thanks
    browse.comment.react(token1, comment_ids[1])
    browse.comment.react(token3, comment_ids[1])
    browse.comment.react(token2, comment_ids[1])

    comments = browse.post.view(token1, post_id)["comments"]
    correct_order = [
        comment_ids[2],
        comment_ids[1],
        comment_ids[0],
        comment_ids[4],
        comment_ids[3],
    ]

    assert comments == correct_order


def test_answered_queue(
    simple_users: ISimpleUsers
):
    """
    Does marking a comment as accepted send the post to the answered queue?
    Does marking the accepted comment as unaccepted send the post back
    to the main queue?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = browse.post.create(user_token, "head", "text", [])["post_id"]

    comment_id = browse.comment.create(
        mod_token, post_id, "first")["comment_id"]

    # Accepting a comment sends the post to the answered queue
    browse.comment.accept(user_token, comment_id)
    post_queue_name = browse.post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.ANSWERED_QUEUE

    queue_id = get_queue(
        queue_list(mod_token)['queues'],
        consts.ANSWERED_QUEUE
    )["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]

    # Un-accepting the accepted comment sends the post to the main queue
    browse.comment.accept(user_token, comment_id)
    post_queue_name = browse.post.view(user_token, post_id)["queue"]
    assert post_queue_name == consts.MAIN_QUEUE

    queue_id = get_queue(
        queue_list(mod_token)['queues'],
        consts.MAIN_QUEUE
    )["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]
