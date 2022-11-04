"""
# Tests / Integration / Browse / Comment View / Accept

Tests for comment view routes

"""
import pytest
from backend.util import http_errors
from ensemble_request.browse import (
    add_comment,
    get_comment,
    post_view,
    accept_comment,
    post_create
)
from tests.integration.conftest import IAllUsers


def test_get_comment_success(
    all_users: IAllUsers,
):
    """
    Can we mark a comment as accepted?
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]
    admin_token = all_users["admins"][0]["token"]
    mod_token = all_users["mods"][0]["token"]

    post_id = post_create(user_token1, "head", "text", [])["post_id"]
    comment_text = "first"
    comment_id = add_comment(user_token1, post_id, comment_text)["comment_id"]

    post = post_view(user_token1, post_id)
    comment = get_comment(user_token1, comment_id)

    # Post author can mark comment as accepted
    assert not post["answered"]
    assert not comment["accepted"]
    assert accept_comment(user_token1, comment_id)["accepted"]
    post = post_view(user_token1, post_id)
    comment = get_comment(user_token1, comment_id)
    assert post["answered"]
    assert comment["accepted"]

    # Admin can mark comment as accepted
    assert not accept_comment(admin_token, comment_id)["accepted"]
    post = post_view(admin_token, post_id)
    comment = get_comment(admin_token, comment_id)
    assert not post["answered"]
    assert not comment["accepted"]
    accept_comment(admin_token, comment_id)
    post = post_view(admin_token, post_id)
    comment = get_comment(admin_token, comment_id)
    assert post["answered"]
    assert comment["accepted"]

    # Mod can mark comment as accepted
    accept_comment(mod_token, comment_id)
    post = post_view(mod_token, post_id)
    comment = get_comment(mod_token, comment_id)
    assert not post["answered"]
    assert not comment["accepted"]
    accept_comment(mod_token, comment_id)
    post = post_view(mod_token, post_id)
    comment = get_comment(mod_token, comment_id)
    assert post["answered"]
    assert comment["accepted"]

    with pytest.raises(http_errors.Forbidden):
        accept_comment(user_token2, comment_id)
