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
from ..request.user import profile
from ..conftest import IAllUsers


def test_view_own_profile(all_users: IAllUsers):
    """Can we view our own profile?"""
    assert profile(
        all_users['users'][0]['token'],
        all_users['users'][0]['user_id'],
    ) == {
        "name_first": "User",
        "name_last": "Ator",
        "username": "user1",
        "email": "user1@example.com",
        "user_id": all_users['users'][0]['user_id'],
    }


def test_view_other_profile(all_users: IAllUsers):
    """Can we view our own profile?"""
    assert profile(
        all_users['users'][0]['token'],
        all_users['users'][1]['user_id'],
    ) == {
        "name_first": "User2",
        "name_last": "Ator",
        "username": "user2",
        "email": "user2@example.com",
        "user_id": all_users['users'][1]['user_id'],
    }


def test_view_invalid_id(all_users: IAllUsers):
    """Do we get a BadRequest when we try to view the profile of an invalid
    user?
    """
    with pytest.raises(http_errors.BadRequest):
        profile(all_users['users'][0]['token'], UserId(-1))
