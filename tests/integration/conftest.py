"""
tests > backend > conftest

Configuration for tests
"""
import pytest
from typing import TypedDict
from backend.types.identifiers import UserId
from backend.types.permissions import PermissionGroupId
from backend.types.auth import JWT
from mock.auth import AUTH_URL
from tests.integration.request.debug import clear
from .request.admin import init


@pytest.fixture(autouse=True)
def before_each():
    """Clear the database between tests"""
    clear()


class IBasicServerSetup(TypedDict):
    username: str
    password: str
    email: str
    user_id: UserId
    token: JWT
    admin_permission: PermissionGroupId
    mod_permission: PermissionGroupId
    user_permission: PermissionGroupId


@pytest.fixture()
def basic_server_setup(before_each) -> IBasicServerSetup:
    """
    Initialise the server and create one admin account
    """
    username = "admin1"
    password = "admin1"
    email = "admin@example.com"
    result = init(
        address=f"{AUTH_URL}/login",
        request_type="get",
        username_param="username",
        password_param="password",
        success_regex="true",
        username=username,
        password=password,
        email=email,
        name_first="Dee",
        name_last="Snuts",
    )
    return {
        "username": username,
        "password": password,
        "email": email,
        "user_id": result["user_id"],
        "token": result["token"],
        # TODO: do a request to actually get these IDs, so things don't break
        # if we change them
        "admin_permission": PermissionGroupId(1),
        "mod_permission": PermissionGroupId(2),
        "user_permission": PermissionGroupId(3),
    }
