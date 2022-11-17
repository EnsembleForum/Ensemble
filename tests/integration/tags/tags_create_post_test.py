"""
# Tests / Integration / Tags / Post Add Tag
# Tests / Integration / Tags / Post Delete Tag

Tests for adding/deleting tags to a post

"""
from tests.integration.conftest import IBasicServerSetup
from ensemble_request.browse import post
from ensemble_request.tags import (
    new_tag,
)


def test_add_tag_to_post_success(
    basic_server_setup: IBasicServerSetup,
):
    """
    Can we create a post with tags using post.create?
    """
    token = basic_server_setup["token"]
    tag1_id = new_tag(token, "tag1")["tag_id"]
    tag2_id = new_tag(token, "tag2")["tag_id"]
    post_id = post.create(
        token, "heading", "text", [tag1_id, tag2_id]
    )["post_id"]

    post_tags = post.view(token, post_id)["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag2_id])

    post_tags = post.list(token)["posts"][0]["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag2_id])


def test_post_edit_tags(
    basic_server_setup: IBasicServerSetup,
):
    """
    Can we create a post with tags using post.create?
    """
    token = basic_server_setup["token"]
    tag1_id = new_tag(token, "tag1")["tag_id"]
    tag2_id = new_tag(token, "tag2")["tag_id"]
    tag3_id = new_tag(token, "tag3")["tag_id"]
    post_id = post.create(
        token, "heading", "text", [tag1_id, tag2_id]
    )["post_id"]

    post.edit(
        token, post_id, "heading1", "text", [tag1_id, tag3_id]
    )

    post_tags = post.view(token, post_id)["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag3_id])

    post_tags = post.list(token)["posts"][0]["tags"]
    assert sorted(post_tags) == sorted([tag1_id, tag3_id])
