"""
# Tests / Integration / Admin / Exam Mode

Tests for admin/exam_mode

* Exam mode is off by default when forum is initialised
* User and mods cannot turn on exam mode
* Admin can toggle exam mode
* User can only post privately during exam mode
* Mod can post privately and publicly during exam mode
"""
import pytest
from tests.integration.conftest import (
    IBasicServerSetup,
    ISimpleUsers,
)
from ensemble_request.browse import (
    post_create,
    post_list
)
from backend.util import http_errors
from ensemble_request.admin.exam_mode import exam_is_enabled, toggle_exam_mode


def test_exam_mode_forum_initialisation(basic_server_setup: IBasicServerSetup):
    """
    Is exam mode off when the forum is initialised?
    """
    token = basic_server_setup['token']
    assert not exam_is_enabled(token)["is_enabled"]


def test_user_no_permission(simple_users: ISimpleUsers):
    """
    User cannot set exam mode
    """
    user_token = simple_users["user"]["token"]
    with pytest.raises(http_errors.Forbidden):
        toggle_exam_mode(user_token)


def test_mod_no_permission(simple_users: ISimpleUsers):
    """
    Mod cannot set exam mode
    """
    mod_token = simple_users["mod"]["token"]
    with pytest.raises(http_errors.Forbidden):
        toggle_exam_mode(mod_token)


def test_admin_toggle_success(simple_users: ISimpleUsers):
    """
    Admin can successfully toggle exam mode on or off
    """
    admin_token = simple_users["admin"]["token"]

    toggle_exam_mode(admin_token)
    assert exam_is_enabled(admin_token)["is_enabled"]

    toggle_exam_mode(admin_token)
    assert not exam_is_enabled(admin_token)["is_enabled"]


def test_user_post_during_exam_mode(simple_users: ISimpleUsers):
    """
    User can only post privately during exam mode
    """
    user_token = simple_users["user"]["token"]
    admin_token = simple_users["admin"]["token"]

    # User cannot post publicly during exam mode
    toggle_exam_mode(admin_token)
    with pytest.raises(http_errors.Forbidden):
        post_create(user_token, 'heading', 'text', [], private=False)

    # User can post privately during exam mode
    post_create(user_token, "First head", "First text", [], private=True)
    assert len(post_list(user_token)["posts"]) == 1


def test_mod_post_during_exam_mode(simple_users: ISimpleUsers):
    """
    Mod can post publicly during exam mode
    """
    mod_token = simple_users["mod"]["token"]
    admin_token = simple_users["admin"]["token"]

    toggle_exam_mode(admin_token)

    post_create(mod_token, 'heading', 'text', [], private=False)
    assert len(post_list(mod_token)["posts"]) == 1
