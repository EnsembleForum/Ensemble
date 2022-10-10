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
from tests.integration.request.admin import users
from tests.integration.conftest import IBasicServerSetup


def test_register_single_user(basic_server_setup: IBasicServerSetup):
    """Can we register a single user"""
    reg = users.register(
        basic_server_setup["token"],
        [{
            "name_first": "Henry",
            "name_last": "VIII",
            "username": "henry8",
            "email": "henry@example.com",
        }],
        basic_server_setup["admin_permission"],
    )
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 1
    assert all[0]["user_id"] == reg["user_ids"][0]


def test_register_multi_users(basic_server_setup: IBasicServerSetup):
    """Can we register multiple users"""
    reg = users.register(
        basic_server_setup["token"],
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
        basic_server_setup["admin_permission"],
    )
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 2
    assert all[0]["user_id"] == reg["user_ids"][0]
    assert all[1]["user_id"] == reg["user_ids"][1]
