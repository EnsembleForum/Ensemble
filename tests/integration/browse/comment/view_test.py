"""
# Tests / Integration / Browse / Comment View

Tests for comment view routes

"""
import pytest
from typing import cast
from backend.types.identifiers import CommentId
from backend.util import http_errors
from ensemble_request.browse import comment
from tests.integration.conftest import ISimpleUsers, IMakePosts


def test_invalid_comment_id(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    If we are given an invalid comment_id, do we get a 400 error?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_id1 = comment.create(token, post_id, "first")["comment_id"]
    invalid_comment_id = cast(CommentId, comment_id1 + 1)
    with pytest.raises(http_errors.BadRequest):
        comment.view(token, invalid_comment_id)


@pytest.mark.core
def test_success(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Can we get the full details of a valid comment?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    comment_text = "first"
    comment_id = comment.create(token, post_id, comment_text)["comment_id"]

    c = comment.view(token, comment_id)
    assert c["text"] == comment_text
    assert c["replies"] == []
    assert isinstance(c["timestamp"], int)
    assert c["thanks"] == 0
