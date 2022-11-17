"""
# Tests / Integration / Tags / New Tag

Tests for creating new tags

"""
import pytest
from tests.integration.conftest import ISimpleUsers, IBasicServerSetup
from backend.util import http_errors
from backend.types.identifiers import TagId
from ensemble_request.tags import (
    get_tag,
    new_tag,
    tags_list
)


def test_get_tag_success(
    simple_users: ISimpleUsers,
):
    """
    Successful creation of 2 tags by the admin
    """

    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    tag1_id = new_tag(admin_token, "tag1")["tag_id"]
    tag1 = get_tag(user_token, tag1_id)

    tag2_id = new_tag(admin_token, "tag2")["tag_id"]
    tag2 = get_tag(user_token, tag2_id)

    assert tag1 == {
        "tag_id": tag1_id,
        "name": "tag1",
    }
    assert tag2 == {
        "tag_id": tag2_id,
        "name": "tag2",
    }
    tags = tags_list(user_token)["tags"]
    assert len(tags) == 2
    assert tag1 in tags
    assert tag2 in tags


def test_no_permission_create(
    simple_users: ISimpleUsers,
):
    """
    A non admin tries to create a tag and fails
    """
    token = simple_users["user"]["token"]
    with pytest.raises(http_errors.Forbidden):
        new_tag(token, "tag1")


def test_duplicate_tag(
    basic_server_setup: IBasicServerSetup,
):
    """
    Cannot create tag that already exists
    """
    token = basic_server_setup["token"]
    new_tag(token, "tag1")
    with pytest.raises(http_errors.BadRequest):
        new_tag(token, "tag1")


def test_invalid_tag_id(
    basic_server_setup: IBasicServerSetup,
):
    """
    Getting a tag fails when tag_id is invalid
    """
    token = basic_server_setup["token"]
    with pytest.raises(http_errors.BadRequest):
        get_tag(token, TagId(-1))
