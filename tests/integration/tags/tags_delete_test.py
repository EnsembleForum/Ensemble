"""
# Tests / Integration / Browse / Tag View

Tests for tag view routes

"""
import pytest
from tests.integration.conftest import ISimpleUsers, IBasicServerSetup
from backend.util import http_errors
from ensemble_request.browse import post
from ensemble_request.tags import (
    new_tag,
    delete_tag,
    tags_list
)


def test_delete_tag_success(
    basic_server_setup: IBasicServerSetup,
):
    """
    Deletion of tag from database
    """
    token = basic_server_setup["token"]
    tag_id = new_tag(token, "tag1")["tag_id"]
    delete_tag(token, tag_id)
    assert len(tags_list(token)["tags"]) == 0


def test_no_permission(
    simple_users: ISimpleUsers,
):
    """
    User and mod cannot delete tag from database
    """
    admin_token = simple_users["admin"]["token"]
    mod_token = simple_users["mod"]["token"]
    user_token = simple_users["user"]["token"]
    tag_id = new_tag(admin_token, "tag1")["tag_id"]

    with pytest.raises(http_errors.Forbidden):
        delete_tag(mod_token, tag_id)

    with pytest.raises(http_errors.Forbidden):
        delete_tag(user_token, tag_id)


def test_del_tag_database_remove_from_post(
    basic_server_setup: IBasicServerSetup,
):
    """
    Can we delete tags from a post successfully and does post_view & post_list
    show the tags correctly?
    """
    token = basic_server_setup["token"]
    tag_id = new_tag(token, "tag1")["tag_id"]
    post_id = post.create(token, "heading", "text", [tag_id])["post_id"]

    delete_tag(token, tag_id)

    assert post.view(token, post_id)["tags"] == []

    assert post.list(token)["posts"][0]["tags"] == []
