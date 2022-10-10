"""
# Tests / Integration / Admin / Users

Tests for bulk registering users

## Register
* Single user
* Multiple users (includes unique IDs)
* Invalid usernames (non-alphanumeric)
* Invalid emails
* Duplicate usernames (none get registered)
* Duplicate emails (none get registered)
* Existing duplicate usernames (none get registered)
* Existing duplicate emails (none get registered)
* Invalid names (empty)
* Don't have permission  # TODO
"""
import pytest
from backend.util import http_errors
from tests.integration.request.admin import users
from tests.integration.conftest import IBasicServerSetup


def test_register_single_user(basic_server_setup: IBasicServerSetup):
    """Can we register a single user?"""
    reg = users.register(
        basic_server_setup["token"],
        [{
            "name_first": "Henry",
            "name_last": "VIII",
            # Even though the username won't work with the mock auth system,
            # it'll still work for registering, as there is no way to check for
            # valid usernames until they try to log in. Don't copy-paste this
            # for tests that require a login. Instead, use on of the fixtures
            # for it
            "username": "henry8",
            "email": "henry@example.com",
        }],
        basic_server_setup["admin_permission"],
    )
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 2
    assert all[1]["user_id"] == reg["user_ids"][0]


def test_register_multi_users(basic_server_setup: IBasicServerSetup):
    """Can we register multiple users?"""
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
    assert len(all) == 3
    assert all[1]["user_id"] == reg["user_ids"][0]
    assert all[2]["user_id"] == reg["user_ids"][1]
    # Do they have unique IDs?
    assert reg["user_ids"][0] != reg["user_ids"][1]


@pytest.mark.parametrize(
    'username',
    [
        'u$ern@me',  # special chars
        'white space',  # whitespace
    ]
)
def test_invalid_usernames(
    basic_server_setup: IBasicServerSetup,
    username: str,
):
    """Does it fail if usernames are invalid?"""
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [{
                "name_first": "Henry",
                "name_last": "VIII",
                "username": username,
                "email": "henry@example.com",
            }],
            basic_server_setup["admin_permission"],
        )
    all = users.all(basic_server_setup["token"])["users"]
    # Only the main user
    assert len(all) == 1


def test_invalid_email(basic_server_setup: IBasicServerSetup):
    """Does it fail if emails are invalid?"""
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [{
                "name_first": "Henry",
                "name_last": "VIII",
                "username": "henry8",
                "email": "henry_example_com",
            }],
            basic_server_setup["admin_permission"],
        )
    all = users.all(basic_server_setup["token"])["users"]
    # Only the main user
    assert len(all) == 1


def test_duplicate_usernames(basic_server_setup: IBasicServerSetup):
    """Does it fail if usernames are duplicate?"""
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [
                {
                    "name_first": "Henry",
                    "name_last": "VIII",
                    "username": "henry8",
                    "email": "henry@example.com",
                },
                {
                    "name_first": "Henry",
                    "name_last": "VIII",
                    "username": "henry8",  # duplicate
                    "email": "henry2@example.com",
                },
            ],
            basic_server_setup["admin_permission"],
        )
    # Only the main user is registered
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 1


def test_duplicate_emails(basic_server_setup: IBasicServerSetup):
    """Does it fail if emails are duplicate?"""
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [
                {
                    "name_first": "Henry",
                    "name_last": "VIII",
                    "username": "henry8",
                    "email": "henry@example.com",
                },
                {
                    "name_first": "Henry",
                    "name_last": "VIII",
                    "username": "henry8_2",
                    "email": "henry@example.com",  # duplicate
                },
            ],
            basic_server_setup["admin_permission"],
        )
    # Only the main user is registered
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 1


def test_existing_duplicate_usernames(basic_server_setup: IBasicServerSetup):
    """Does it fail if an existing username is already registered?"""
    users.register(
        basic_server_setup["token"],
        [
            {
                "name_first": "Henry",
                "name_last": "VIII",
                "username": "henry8",
                "email": "henry@example.com",
            },
        ],
        basic_server_setup["admin_permission"],
    )
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [
                {
                    "name_first": "Henry",
                    "name_last": "VIII",
                    "username": "henry8",  # duplicate
                    "email": "henry2@example.com",
                },
            ],
            basic_server_setup["admin_permission"],
        )
    # Only the first user got registered
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 2


def test_existing_duplicate_emails(basic_server_setup: IBasicServerSetup):
    """Does it fail if an existing email is already registered?"""
    users.register(
        basic_server_setup["token"],
        [
            {
                "name_first": "Henry",
                "name_last": "VIII",
                "username": "henry8",
                "email": "henry@example.com",
            },
        ],
        basic_server_setup["admin_permission"],
    )
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [
                {
                    "name_first": "Henry",
                    "name_last": "VIII",
                    "username": "henry8_2",
                    "email": "henry@example.com",  # duplicate
                },
            ],
            basic_server_setup["admin_permission"],
        )
    # Only the first user got registered
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 2


def test_invalid_name_first(basic_server_setup: IBasicServerSetup):
    """Does it fail to register a user with empty first name?"""
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [{
                "name_first": "Henry",
                "name_last": "",
                "username": "henry8",
                "email": "henry8@example.com",
            }],
            basic_server_setup["admin_permission"],
        )
    # Only the main user is registered
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 1


def test_invalid_name_last(basic_server_setup: IBasicServerSetup):
    """Does it fail to register a user with empty last name?"""
    with pytest.raises(http_errors.BadRequest):
        users.register(
            basic_server_setup["token"],
            [{
                "name_first": "",
                "name_last": "VIII",
                "username": "henry8",
                "email": "henry8@example.com",
            }],
            basic_server_setup["admin_permission"],
        )
    # Only the main user is registered
    all = users.all(basic_server_setup["token"])["users"]
    assert len(all) == 1
