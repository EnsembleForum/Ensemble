"""
# Tests / Integration / Browse / Tag View

Tests for tag view routes

"""
import pytest
from typing import cast
from ..conftest import ISimpleUsers, IMakePosts
from backend.types.identifiers import ReplyId
from backend.types.tag import ITagBasicInfo, ITagId
from backend.util import http_errors
from ensemble_request.browse import (
    get_tag,
    create_tag,
    delete_tag,
    add_tag_to_post,
    remove_tag_from_post,
)
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts
)
from typing import cast

def test_create_tag(
    simple_users: ISimpleUsers,
):
    """
    Successful reaction by one user
    """
    token = simple_users["admin"]["token"]
    tag1 = cast(ITagId, create_tag(token, "tag1"))
    assert tag1 == {"tag_id": 1}
