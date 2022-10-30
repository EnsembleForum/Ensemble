"""
# Tests / Integration / Browse / Post View / Self Delete

Tests for post_view/self_delete

* Fails when trying to delete another user's post
* Succeeds when deleting a post with no comments
* Succeeds when deleting a post
    * Also deletes its comments, and the replies to those comments
"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    add_reply,
    get_reply,
    post_delete,
    post_list,
    post_view,
    add_comment,
    get_comment,
)
from tests.integration.conftest import (
    ISimpleUsers,
    IBasicServerSetup,
    IMakePosts,
)


def test_delete_other_user_post(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does deleting another person's post raise a 403 error
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.Forbidden):
        post_delete(token, make_posts["post1_id"])


def test_delete_success(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Successful deletion of one of the posts
    """
    token = basic_server_setup["token"]
    post_delete(token, make_posts["post1_id"])
    with pytest.raises(http_errors.BadRequest):
        post_view(token, make_posts["post1_id"])

    posts = post_list(token)
    assert len(posts["posts"]) == 1
    assert posts["posts"][0]["post_id"] == make_posts["post2_id"]


def test_delete_post_deletes_comments(
    basic_server_setup: IBasicServerSetup,
    make_posts: IMakePosts,
):
    """
    Delete a post containing two comments
    The two comments should also be deleted
    """
    token = basic_server_setup["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = add_comment(token, post_id, "first")["comment_id"]
    comment_id2 = add_comment(token, post_id, "second")["comment_id"]
    reply_id = add_reply(token, comment_id1, "reply_text")["reply_id"]

    post_delete(token, make_posts["post1_id"])

    with pytest.raises(http_errors.BadRequest):
        get_comment(token, comment_id1)

    with pytest.raises(http_errors.BadRequest):
        get_comment(token, comment_id2)

    with pytest.raises(http_errors.BadRequest):
        get_reply(token, reply_id)
