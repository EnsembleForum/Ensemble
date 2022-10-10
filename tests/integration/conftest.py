"""
tests > backend > conftest

Configuration for tests
"""
import pytest
from typing import TypedDict
from backend.types.identifiers import UserId, PostId
from backend.types.auth import JWT
from mock.auth import AUTH_URL
from tests.integration.request.debug import clear
from tests.integration.request.browse import post_create
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
    name_first: str
    name_last: str


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
        "name_first": "Dee",
        "name_last": "Snuts",
    }


class ITwoPosts(TypedDict):
    post1_id: PostId
    post2_id: PostId
    head1: str
    head2: str
    text1: str
    text2: str


@pytest.fixture()
def create_two_posts(basic_server_setup: IBasicServerSetup) -> ITwoPosts:
    """
    Create two posts inside the forum
    """
    token = basic_server_setup["token"]
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