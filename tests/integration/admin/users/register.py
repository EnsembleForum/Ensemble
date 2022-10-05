"""
# Tests / Integration / Admin / Users

Tests for bulk registering users

## Register
* Single user
* Multiple users (includes unique IDs)
* Invalid usernames (capitals)
* Duplicate usernames (none registered)
* Duplicate emails (none registered)
* Existing usernames (none registered)
* Existing emails (none registered)
"""
from tests.integration.constructors import basic_permission_group
from tests.integration.functions.admin import users


def test_register_single_user():
    """Can we register a single user"""
    group = basic_permission_group()
    user = users.register(
        [{
            "name_first": "Henry",
            "name_last": "VIII",
            "username": "henry8",
            "email": "henry@example.com",
        }],
        group,
    )
    new_users = users.all()["users"]
    assert len(new_users) == 1
    assert new_users[0]["user_id"] == user["user_ids"][0]


def test_register_multi_users():
    """Can we register multiple users"""
    group = basic_permission_group()
    user = users.register(
        [
            {
                "name_first": "Henry",
                "name_last": "VIII",
                "username": "henry8",
                "email": "henry8@example.com",
            },
            {
                "name_first": "Henry",
                "name_last": "IX",
                "username": "henry9",
                "email": "henry9@example.com",
            },
        ],
        group,
    )
    new_users = users.all()["users"]
    assert len(new_users) == 2
    assert new_users[0]["user_id"] == user["user_ids"][0]
