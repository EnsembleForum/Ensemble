"""
# Tests / Integration / Profile edit test

Tests for editing a user profile

* Edit own profile (for all profile edit routes)
* Mod can't edit profile (for all profile edit routes)
* Admin can edit profile (for all profile edit routes)
* Can't edit invalid profile (for all profile edit routes)
* Can't edit own profile if no permission (for all profile edit routes)
* Can set pronouns to None
"""

from typing import Any, Callable, cast
import pytest
from backend.models.permissions.permission import Permission
from backend.util import http_errors
from backend.types.auth import JWT
from backend.types.identifiers import UserId
from ensemble_request.user import (
    profile,
    profile_edit_name_first,
    profile_edit_name_last,
    profile_edit_email,
    profile_edit_pronouns,
)
from ensemble_request.admin import permissions
from ..conftest import (
    ISimpleUsers,
    IBasicServerSetup,
    IPermissionGroups,
)


ProfileEditCallback = Callable[[JWT, UserId, str], None]
"""Type annotation for profile edit functions"""


test_params = (
    ('callback', 'new_key', 'new_value'),
    [
        (profile_edit_name_first, 'name_first', 'Robin'),
        (profile_edit_name_last, 'name_last', 'Banks'),
        (profile_edit_email, 'email', 'robin.banks@bigpond.com.au'),
        (profile_edit_pronouns, 'pronouns', 'He/him'),
    ],
)


@pytest.mark.parametrize(*test_params)
def test_user_can_edit_own(
    callback: ProfileEditCallback,
    new_key: str,
    new_value: str,
    simple_users: ISimpleUsers,
):
    """Users can edit their own profiles"""
    user_id = simple_users['user']['user_id']
    token = simple_users['user']['token']
    # Get profile before edit
    p = cast(dict[str, Any], profile(token, user_id))
    # Perform the edit
    callback(
        token,
        user_id,
        new_value,
    )
    p[new_key] = new_value
    assert p == profile(token, user_id)


@pytest.mark.parametrize(*test_params)
def test_user_cant_edit_others(
    callback: ProfileEditCallback,
    new_key: str,
    new_value: str,
    simple_users: ISimpleUsers,
):
    """
    Standard users and mods shouldn't be able to edit other people's profiles
    """
    with pytest.raises(http_errors.Forbidden):
        callback(
            simple_users["mod"]["token"],
            simple_users["user"]["user_id"],
            new_value,
        )


@pytest.mark.parametrize(*test_params)
def test_admin_can_edit_others(
    callback: ProfileEditCallback,
    new_key: str,
    new_value: str,
    simple_users: ISimpleUsers,
):
    """Admins can edit other people's profiles"""
    user_id = simple_users['user']['user_id']
    token = simple_users['admin']['token']
    # Get profile before edit
    p = cast(dict[str, Any], profile(token, user_id))
    # Perform the edit
    callback(
        token,
        user_id,
        new_value,
    )
    p[new_key] = new_value
    assert p == profile(token, user_id)


@pytest.mark.parametrize(*test_params)
def test_cant_edit_invalid_profile(
    callback: ProfileEditCallback,
    new_key: str,
    new_value: str,
    basic_server_setup: IBasicServerSetup,
):
    """
    We should get an error if we try to edit a profile that doesn't exist
    """
    with pytest.raises(http_errors.BadRequest):
        callback(
            basic_server_setup["token"],
            UserId(-1),
            new_value,
        )


@pytest.mark.parametrize(*test_params)
def test_cant_edit_invalid_new_value(
    callback: ProfileEditCallback,
    new_key: str,
    new_value: str,
    basic_server_setup: IBasicServerSetup,
):
    """
    We should get an error if we try to edit a profile to use an empty string
    """
    with pytest.raises(http_errors.BadRequest):
        callback(
            basic_server_setup["token"],
            basic_server_setup["user_id"],
            "",
        )


@pytest.mark.parametrize(*test_params)
def test_cant_edit_own_profile_without_permission(
    callback: ProfileEditCallback,
    new_key: str,
    new_value: str,
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """
    We should get an error if we try to edit a profile that doesn't exist
    """
    # Disable users editing their own profile
    permissions.groups_edit(
        simple_users["admin"]["token"],
        permission_groups["user"]["group_id"],
        "User",
        [
            (
                # Change EditProfile to False
                p  # type: ignore
                if p["permission_id"] != Permission.EditProfile.value
                else p | {"value": False})
            for p in permission_groups["user"]["permissions"]
        ]
    )
    with pytest.raises(http_errors.Forbidden):
        callback(
            simple_users["user"]["token"],
            simple_users["user"]["user_id"],
            new_value,
        )


def test_set_null_pronouns(basic_server_setup: IBasicServerSetup):
    """We should be able to set a user's pronouns to None"""
    profile_edit_pronouns(
        basic_server_setup['token'],
        basic_server_setup['user_id'],
        "They/them",
    )
    profile_edit_pronouns(
        basic_server_setup['token'],
        basic_server_setup['user_id'],
        None,
    )
    assert profile(
        basic_server_setup['token'],
        basic_server_setup['user_id'],
    )['pronouns'] is None
