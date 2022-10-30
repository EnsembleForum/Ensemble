"""
# Tests / Integration / Admin / Users / All

Tests for listing all users

## Test List
* Correct info returned
* Works for many users
* Fails for unauthorised user
"""
import pytest
from backend.util import http_errors
from ensemble_request.admin import users
from tests.integration.conftest import IBasicServerSetup, ISimpleUsers


def test_single_user(basic_server_setup: IBasicServerSetup):
    """Do we get the correct info for a single user being registered?"""
    assert users.all(basic_server_setup['token']) == {
        "users": [{
            "name_first": "Dee",
            "name_last": "Snuts",
            "username": "admin1",
            "user_id": basic_server_setup["user_id"],
        }]
    }


def test_returns_all(simple_users: ISimpleUsers):
    """Are the correct number of users returned?"""
    assert len(users.all(simple_users["admin"]["token"])["users"]) == 3


def test_unauthorised(simple_users: ISimpleUsers):
    """Do we fail to get the info if we don't have permission?"""
    with pytest.raises(http_errors.Forbidden):
        users.all(simple_users["user"]["token"])
