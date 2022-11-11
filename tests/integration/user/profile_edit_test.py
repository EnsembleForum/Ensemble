"""
# Tests / Integration / Profile edit test

Tests for editing a user profile

* Edit a user's name
"""

import pytest
from backend.util import http_errors
from ensemble_request.user import profile_edit_first, profile_edit_last
from ..conftest import (
    IAllUsers,
)


def test_edit_own_profile_first(all_users: IAllUsers):
    """Can we edit our own profile?"""
    user = all_users['users'][0]
    user_id = user['user_id']
    token = user['token']
    new_first_name = 'newFirstname'
    assert profile_edit_first(
        token,
        user_id,
        new_first_name
    ) == {
        "name_first": "newFirstname",
        "name_last": "Ator",
        "username": "user1",
        "email": "user1@example.com",
        "pronoun": "he/him",
        "user_id": all_users['users'][0]['user_id'],
    }


def test_edit_own_profile_last(all_users: IAllUsers):
    """Can we edit our own profile?"""
    user = all_users['users'][0]
    user_id = user['user_id']
    token = user['token']
    new_last_name = 'newLastname'
    assert profile_edit_last(
        token,
        user_id,
        new_last_name
    ) == {
        "name_first": "User",
        "name_last": "newLastname",
        "username": "user1",
        "email": "user1@example.com",
        "pronoun": "he/him",
        "user_id": all_users['users'][0]['user_id'],
    }

def test_edit_other_first_name(all_users: IAllUsers):
    user1 = all_users["users"][0]
    user1_id = user1['user_id']
    token1 = all_users["users"][0]["token"]
    user2 = all_users["users"][1]
    user2_id = user2['user_id']
    token2 = all_users["users"][1]["token"]
    new_first_name = "hello world"
    with pytest.raises(http_errors.Forbidden):
        profile_edit_first(
            token1,
            user2_id,
            new_first_name,
        )
