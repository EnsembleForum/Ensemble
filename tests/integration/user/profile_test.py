"""
# Tests / Integration / Profile test

Tests for user profile route

* View own profile
* View other profile
* View invalid ID
"""
import pytest
from backend.util import http_errors
from backend.types.identifiers import UserId
from ensemble_request.user import profile
from ..conftest import ISimpleUsers


def test_view_own_profile(simple_users: ISimpleUsers):
    """Can we view our own profile?"""
    assert profile(
        simple_users['user']['token'],
        simple_users['user']['user_id'],
    ) == {
        "name_first": "User",
        "name_last": "Ator",
        "username": "user1",
        "email": "user1@example.com",
        "pronouns": None,
        "user_id": simple_users['user']['user_id'],
        "permission_group": "User"
    }


@pytest.mark.core
def test_view_other_profile(simple_users: ISimpleUsers):
    """Can we view our own profile?"""
    assert profile(
        simple_users['user']['token'],
        simple_users['mod']['user_id'],
    ) == {
        "name_first": "Mod",
        "name_last": "Erator",
        "username": "mod1",
        "email": "mod1@example.com",
        "pronouns": None,
        "user_id": simple_users['mod']['user_id'],
        "permission_group": "Mod"
    }


def test_view_invalid_id(simple_users: ISimpleUsers):
    """Do we get a BadRequest when we try to view the profile of an invalid
    user?
    """
    with pytest.raises(http_errors.BadRequest):
        profile(simple_users['user']['token'], UserId(-1))
