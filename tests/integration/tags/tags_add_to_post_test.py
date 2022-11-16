"""
# Tests / Integration / Tags / Post Add Tag
# Tests / Integration / Tags / Post Delete Tag

Tests for adding/deleting tags to a post

"""
from tests.integration.conftest import IBasicServerSetup
from ensemble_request.browse import post
from ensemble_request.tags import (
    create_tag,
    add_tag_to_post,
    remove_tag_from_post,
)


def test_add_tag_to_post_success(
    basic_server_setup: IBasicServerSetup,
):
    """
    Can we add tags to a post successfully and does post_view & post_list
    show the tags correctly?
    """
    token = basic_server_setup["token"]
    tag1_id = create_tag(token, "tag1")["tag_id"]
    tag2_id = create_tag(token, "tag2")["tag_id"]
    post_id = post.create(token, "heading", "text", [])["post_id"]

    assert add_tag_to_post(token, post_id, tag1_id)["tag_id"] == tag1_id
    assert add_tag_to_post(token, post_id, tag2_id)["tag_id"] == tag2_id

    post_tags = post.view(token, post_id)["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag2_id])

    post_tags = post.list(token)["posts"][0]["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag2_id])


def test_remove_tag_from_post(
    basic_server_setup: IBasicServerSetup,
):
    """
    Can we delete tags from a post successfully and does post_view & post_list
    show the tags correctly?
    """
    token = basic_server_setup["token"]
    tag1_id = create_tag(token, "tag1")["tag_id"]
    tag2_id = create_tag(token, "tag2")["tag_id"]
    tag3_id = create_tag(token, "tag3")["tag_id"]
    post_id = post.create(token, "heading", "text", [])["post_id"]

    add_tag_to_post(token, post_id, tag1_id)
    add_tag_to_post(token, post_id, tag2_id)
    add_tag_to_post(token, post_id, tag3_id)
    remove_tag_from_post(token, post_id, tag3_id)

    post_tags = post.view(token, post_id)["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag2_id])

    post_tags = post.list(token)["posts"][0]["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag2_id])


def test_add_duplicate_tags(
    basic_server_setup: IBasicServerSetup,
):
    """
    Adding the same tag to a post has no effect
    """
    token = basic_server_setup["token"]
    tag_id = create_tag(token, "tag1")["tag_id"]
    post_id = post.create(token, "heading", "text", [])["post_id"]

    add_tag_to_post(token, post_id, tag_id)
    add_tag_to_post(token, post_id, tag_id)

    post_tags = post.view(token, post_id)["tags"]
    assert post_tags == [tag_id]

    post_tags = post.list(token)["posts"][0]["tags"]
    assert post_tags == [tag_id]
