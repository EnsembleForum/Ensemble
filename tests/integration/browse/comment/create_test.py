"""
# Tests / Integration / Browse / Post View / Comment

Tests for post.view/comment

* Fails with empty comment string
* Fails when post trying to comment on does not exist
* Succeeds with valid inputs

"""
import pytest
from typing import cast
from ...conftest import ISimpleUsers, IMakePosts
from backend.types.identifiers import PostId
from backend.util import http_errors
from ensemble_request.browse import (
    post,
    comment,
)


def test_empty_text_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Does creating a comment with empty text raise a 400 error?
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.BadRequest):
        comment.create(token, make_posts["post1_id"], "")


def test_invalid_post_comment(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    When trying to comment under a post whose post_id does not exist,
    is a 400 error raised?
    """
    token = simple_users["user"]["token"]
    invalid_post_id = (
        max(make_posts["post1_id"], make_posts["post2_id"]) + 1
    )
    invalid_post_id = cast(PostId, invalid_post_id)
    with pytest.raises(http_errors.BadRequest):
        comment.create(token, invalid_post_id, "hello")


@pytest.mark.core
def test_add_two_comments(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Add two comments
    List of comment_id returned by post.view should be in order
    of newest to oldest
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = comment.create(token, post_id, "first")["comment_id"]
    comment_id2 = comment.create(token, post_id, "second")["comment_id"]

    p = post.view(token, post_id)
    assert p["comments"] == [comment_id2, comment_id1]
