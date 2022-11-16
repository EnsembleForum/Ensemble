"""
# Tests / Integration / Browse / Tag View

Tests for tag view routes

"""
import pytest
from typing import cast
from tests.integration.conftest import ISimpleUsers
from backend.types.tag import ITagId
from backend.util import http_errors
from ensemble_request.browse import post
from ensemble_request.tags import (
    get_tag,
    create_tag,
    delete_tag,
    add_tag_to_post,
    remove_tag_from_post,
)


def test_get_tag_success(
    simple_users: ISimpleUsers,
):
    """
    Successful getting of tags by one user after an admin makes it
    """

    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    tag1 = create_tag(admin_token, "tag1")
    tag = get_tag(user_token, tag1["tag_id"])
    assert tag == {
        "tag_id": 1,
        "name": 'tag1',
    }


def test_create_tag_success(
    simple_users: ISimpleUsers,
):
    """
    Successful creating of tags by one admin
    """
    token = simple_users["admin"]["token"]
    tag1 = cast(ITagId, create_tag(token, "tag1"))
    assert tag1 == {"tag_id": 1}


def test_create_tag_fail(
    simple_users: ISimpleUsers,
):
    """
    A non admin tries to create a tag and fails
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.Forbidden):
        create_tag(token, "tag1")


def test_delete_tag_success(
    simple_users: ISimpleUsers,
):
    """
    Successful reaction by one user
    """
    token = simple_users["admin"]["token"]
    tag1 = create_tag(token, "tag1")
    delete_tag(token, tag1["tag_id"])


def test_add_tag_to_post_succes(
    simple_users: ISimpleUsers,
):
    token = simple_users["admin"]["token"]
    tag1_id = create_tag(token, "tag1")["tag_id"]
    tag2_id = create_tag(token, "tag2")["tag_id"]
    post_id = post.create(token, "heading", "text", [])["post_id"]

    assert add_tag_to_post(token, post_id, tag1_id) == {
        "tag_id": 1
    }
    assert add_tag_to_post(token, post_id, tag2_id) == {
        "tag_id": 2
    }


def test_remove_tag_from_post(
    simple_users: ISimpleUsers,
):
    token = simple_users["admin"]["token"]
    tag1_id = create_tag(token, "tag1")["tag_id"]
    tag2_id = create_tag(token, "tag2")["tag_id"]
    tag3_id = create_tag(token, "tag2")["tag_id"]
    post_id = post.create(token, "heading", "text", [])["post_id"]

    add_tag_to_post(token, post_id, tag1_id)
    add_tag_to_post(token, post_id, tag2_id)
    add_tag_to_post(token, post_id, tag3_id)
    remove_tag_from_post(token, post_id, tag3_id)
    post_tags = post.view(token, post_id)["tags"]

    assert post_tags == [1, 2]
