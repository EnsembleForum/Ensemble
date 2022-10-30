"""
# Tests / Integration / Profile edit test

Tests for editing a user profile

* Edit a user's name
"""


from ..request.user import profile_edit_first, profile_edit_last
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
