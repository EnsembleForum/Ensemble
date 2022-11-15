"""
# Tests / Integration / Browse / Tag View

Tests for tag view routes

"""
import pytest
from typing import cast
from ..conftest import ISimpleUsers, IMakePosts
from backend.types.identifiers import ReplyId
from backend.util import http_errors
from ensemble_request.browse import (
    get_tag,
    create_tag,
    delete_tag,
    add_tag_to_post,
    remove_tag_from_post,
)
