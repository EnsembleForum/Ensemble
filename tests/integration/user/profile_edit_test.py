"""
# Tests / Integration / Profile edit test

Tests for editing a user profile

* Edit own profile (for all profile edit routes)
* Mod can't edit profile (for all profile edit routes)
* Admin can edit profile (for all profile edit routes)
* Can't edit invalid profile (for all profile edit routes)
* Can set pronouns to None
"""

from typing import Any, Callable, cast
import pytest
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
from ..conftest import (
    ISimpleUsers,
    IBasicServerSetup,
)


ProfileEditCallback = Callable[[JWT, UserId, str], None]
"""Type annotation for profile edit functions"""


@pytest.mark.parametrize(
    ('callback', 'new_key', 'new_value'),
    [
        (profile_edit_name_first, 'name_first', 'Robin'),
        (profile_edit_name_last, 'name_last', 'Banks'),
        (profile_edit_email, 'email', 'robin.banks@bigpond.com.au'),
        (profile_edit_pronouns, 'pronouns', 'He/him'),
    ]
)
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


@pytest.mark.parametrize(
    'callback',
    [
        profile_edit_name_first,
        profile_edit_name_last,
        profile_edit_email,
        profile_edit_pronouns,
    ]
)
def test_user_cant_edit_others(
    callback: ProfileEditCallback,
    simple_users: ISimpleUsers,
):
    """
    Standard users and mods shouldn't be able to edit other people's profiles
    """
    with pytest.raises(http_errors.Forbidden):
        callback(
            simple_users["mod"]["token"],
            simple_users["user"]["user_id"],
            "not allowed",
        )


@pytest.mark.parametrize(
    ('callback', 'new_key', 'new_value'),
    [
        (profile_edit_name_first, 'name_first', 'Robin'),
        (profile_edit_name_last, 'name_last', 'Banks'),
        (profile_edit_email, 'email', 'robin.banks@bigpond.com.au'),
        (profile_edit_pronouns, 'pronouns', 'He/him'),
    ]
)
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


@pytest.mark.parametrize(
    'callback',
    [
        profile_edit_name_first,
        profile_edit_name_last,
        profile_edit_email,
        profile_edit_pronouns,
    ]
)
def test_cant_edit_invalid_profile(
    callback: ProfileEditCallback,
    basic_server_setup: IBasicServerSetup,
):
    """
    We should get an error if we try to edit a profile that doesn't exist
    """
    with pytest.raises(http_errors.BadRequest):
        callback(
            basic_server_setup["token"],
            UserId(-1),
            "bad id",
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
