"""
tests > backend > conftest

Configuration for tests
"""
import pytest
from typing import TypedDict
from backend.types.identifiers import UserId, PostId
from backend.types.permissions import IPermissionGroup
from backend.types.auth import JWT, IAuthInfo
from mock.auth import AUTH_URL
from .request.debug import clear
from .request.admin import init, users
from .request.admin.permissions import groups_list
from .request.auth import login
from .request.browse import post_create


@pytest.fixture(autouse=True)
def before_each():
    """Clear the database between tests"""
    clear()


class IBasicServerSetup(TypedDict):
    """
    Set up the server

    * user_id
    * token
    """
    user_id: UserId
    token: JWT


@pytest.fixture
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
        "user_id": result["user_id"],
        "token": result["token"],
    }


class IPermissionGroups(TypedDict):
    """
    Contains permission info for all pre-defined permission groups

    * admin
    * mod
    * user
    """
    admin: IPermissionGroup
    mod: IPermissionGroup
    user: IPermissionGroup


@pytest.fixture
def permission_groups(
    basic_server_setup: IBasicServerSetup,
) -> IPermissionGroups:
    """
    Represents all available permissions upon initialising the server
    """
    ids = groups_list(basic_server_setup['token'])["groups"]
    assert ids[0]["name"] == "Administrator"
    assert ids[1]["name"] == "Moderator"
    assert ids[2]["name"] == "User"
    return {
        "admin": ids[0],
        "mod": ids[1],
        "user": ids[2],
    }


class IAllUsers(TypedDict):
    """
    Represents all users

    * admins (token, user_id)
    * mods (token, user_id)
    * users (token, user_id)
    """
    admins: list[IAuthInfo]
    mods: list[IAuthInfo]
    users: list[IAuthInfo]


@pytest.fixture
def all_users(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
) -> IAllUsers:
    """
    Register all users available through the mock auth server

    * 3 admins

    * 3 moderators

    * 3 users
    """
    # Admins
    users.register(
        basic_server_setup["token"],
        [
            {
                "username": "admin2",
                "email": "admin2@example.com",
                "name_first": "Admin",
                "name_last": "Istrator",
            },
            {
                "username": "admin3",
                "email": "admin3@example.com",
                "name_first": "Admin3",
                "name_last": "Istrator",
            },
        ],
        permission_groups["admin"]["group_id"],
    )
    # Moderators
    users.register(
        basic_server_setup["token"],
        [
            {
                "username": "mod1",
                "email": "mod1@example.com",
                "name_first": "Mod",
                "name_last": "Erator",
            },
            {
                "username": "mod2",
                "email": "mod2@example.com",
                "name_first": "Mod2",
                "name_last": "Erator",
            },
            {
                "username": "mod3",
                "email": "mod3@example.com",
                "name_first": "Mod3",
                "name_last": "Erator",
            },
        ],
        permission_groups["mod"]["group_id"],
    )
    # Users
    users.register(
        basic_server_setup["token"],
        [
            {
                "username": "user1",
                "email": "user1@example.com",
                "name_first": "User",
                "name_last": "Ator",
            },
            {
                "username": "user2",
                "email": "user2@example.com",
                "name_first": "User2",
                "name_last": "Ator",
            },
            {
                "username": "user3",
                "email": "user3@example.com",
                "name_first": "User3",
                "name_last": "Ator",
            },
        ],
        permission_groups["user"]["group_id"],
    )
    # Log everyone in and return their info
    return {
        "admins": [
            {
                "token": basic_server_setup["token"],
                "user_id": basic_server_setup["user_id"],
            },
            login("admin2", "admin2"),
            login("admin3", "admin3"),
        ],
        "mods": [
            login("mod1", "mod1"),
            login("mod2", "mod2"),
            login("mod3", "mod3"),
        ],
        "users": [
            login("user1", "user1"),
            login("user2", "user2"),
            login("user3", "user3"),
        ],
    }


class ITwoPosts(TypedDict):
    post1_id: PostId
    post2_id: PostId
    head1: str
    head2: str
    text1: str
    text2: str


@pytest.fixture()
def make_posts(all_users) -> ITwoPosts:
    """
    Create two posts inside the forum
    """
    token = all_users["users"][0]["token"]
    head1 = "First head"
    head2 = "Second head"
    text1 = "First text"
    text2 = "Second text"
    post1_id = post_create(token, head1, text1, [])["post_id"]
    post2_id = post_create(token, head2, text2, [])["post_id"]

    return {
        "post1_id": post1_id,
        "post2_id": post2_id,
        "head1": head1,
        "head2": head2,
        "text1": text1,
        "text2": text2,
    }
