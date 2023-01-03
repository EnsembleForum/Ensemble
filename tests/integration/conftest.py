"""
tests > backend > conftest

Configuration for tests
"""
import pytest
from typing import TypedDict
from backend import consts
from backend.types.identifiers import PostId, QueueId
from backend.types.permissions import IPermissionGroup
from backend.types.auth import IAuthInfo
from mock.auth import AUTH_URL
from ensemble_request.debug import clear, echo, unsafe_init, unsafe_login
from ensemble_request.browse import post
from ensemble_request.admin import users
from ensemble_request.admin.permissions import groups_list
from ensemble_request.taskboard import queue_create, queue_list


@pytest.fixture(autouse=True)
def before_each(request: pytest.FixtureRequest):
    """Clear the database between tests"""
    clear()
    echo(f"{request.module.__name__}.{request.function.__name__}")


IBasicServerSetup = IAuthInfo


@pytest.fixture
def basic_server_setup(before_each) -> IBasicServerSetup:
    """
    Initialise the server and create one admin account
    """
    username = "admin1"
    password = "admin1"
    email = "admin@example.com"
    return unsafe_init(
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
    # If these assertions fail, this fixture should be updated
    assert len(ids) == 3
    assert ids[0]["name"] == "Administrator"
    assert ids[1]["name"] == "Moderator"
    assert ids[2]["name"] == "User"
    return {
        "admin": ids[0],
        "mod": ids[1],
        "user": ids[2],
    }


class ISimpleUsers(TypedDict):
    """
    Represents one of each type of user

    * admin (token, user_id)
    * mod (token, user_id)
    * user (token, user_id)
    """
    admin: IAuthInfo
    mod: IAuthInfo
    user: IAuthInfo


@pytest.fixture
def simple_users(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
) -> ISimpleUsers:
    """
    Register all users available through the mock auth server

    * 3 admins

    * 3 moderators

    * 3 users
    """
    # Moderator
    users.register(
        basic_server_setup["token"],
        [{
            "username": "mod1",
            "email": "mod1@example.com",
            "name_first": "Mod",
            "name_last": "Erator",
        }],
        permission_groups["mod"]["group_id"],
    )
    # Users
    users.register(
        basic_server_setup["token"],
        [{
            "username": "user1",
            "email": "user1@example.com",
            "name_first": "User",
            "name_last": "Ator",
        }],
        permission_groups["user"]["group_id"],
    )
    # Log everyone in and return their info
    return {
        "admin": basic_server_setup,
        "mod": unsafe_login("mod1"),
        "user": unsafe_login("user1"),
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
    simple_users: ISimpleUsers,
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
        simple_users["admin"]["token"],
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
        simple_users["admin"]["token"],
        [
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
        simple_users["admin"]["token"],
        [
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
            simple_users["admin"],
            unsafe_login("admin2"),
            unsafe_login("admin3"),
        ],
        "mods": [
            simple_users["mod"],
            unsafe_login("mod2"),
            unsafe_login("mod3"),
        ],
        "users": [
            simple_users["user"],
            unsafe_login("user2"),
            unsafe_login("user3"),
        ],
    }


class IMakePosts(TypedDict):
    """
    Create two posts inside the forum.

    Both posts are created by the admin
    """
    post1_id: PostId
    post2_id: PostId
    head1: str
    head2: str
    text1: str
    text2: str


@pytest.fixture()
def make_posts(basic_server_setup: IBasicServerSetup) -> IMakePosts:
    """
    Create two posts inside the forum.

    Both posts are created by the admin
    """
    token = basic_server_setup["token"]
    head1 = "First head"
    head2 = "Second head"
    text1 = "First text"
    text2 = "Second text"
    post1_id = post.create(token, head1, text1, [])["post_id"]
    post2_id = post.create(token, head2, text2, [])["post_id"]

    return {
        "post1_id": post1_id,
        "post2_id": post2_id,
        "head1": head1,
        "head2": head2,
        "text1": text1,
        "text2": text2,
    }


class IDefaultQueues(TypedDict):
    """
    Get info on the default queues
    """
    main: QueueId
    answered: QueueId
    closed: QueueId
    deleted: QueueId
    reported: QueueId


@pytest.fixture()
def default_queues(basic_server_setup: IBasicServerSetup) -> IDefaultQueues:
    """
    Get info on the default queues
    """
    token = basic_server_setup["token"]
    ids = queue_list(token)["queues"]

    # If these assertions fail, this fixture should be updated
    # Probably we added more default queues, or changed the ordering or
    # something
    assert len(ids) == 5
    assert ids[0]["queue_name"] == consts.MAIN_QUEUE
    assert ids[1]["queue_name"] == consts.REPORTED_QUEUE
    assert ids[2]["queue_name"] == consts.CLOSED_QUEUE
    assert ids[3]["queue_name"] == consts.ANSWERED_QUEUE
    assert ids[4]["queue_name"] == consts.DELETED_QUEUE

    return {
        "main": ids[0]["queue_id"],
        "reported": ids[1]["queue_id"],
        "closed": ids[2]["queue_id"],
        "answered": ids[2]["queue_id"],
        "deleted": ids[4]["queue_id"],
    }


class IMakeQueues(TypedDict):
    """
    Create two queues on the forum
    """
    queue1_id: QueueId
    queue2_id: QueueId
    queue_name1: str
    queue_name2: str


@pytest.fixture()
def make_queues(
    basic_server_setup: IBasicServerSetup,
    default_queues: IDefaultQueues,
) -> IMakeQueues:
    """
    Create two queues inside the forum
    """
    token = basic_server_setup["token"]
    queue_name1 = "First queue"
    queue_name2 = "Second queue"
    queue1_id = queue_create(token, queue_name1)["queue_id"]
    queue2_id = queue_create(token, queue_name2)["queue_id"]

    return {
        "queue1_id": queue1_id,
        "queue2_id": queue2_id,
        "queue_name1": queue_name1,
        "queue_name2": queue_name2
    }
