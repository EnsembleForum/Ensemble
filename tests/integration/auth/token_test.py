"""
# Tests / Integration / Auth / Token test

Tests for tokens
"""
from requests import post as req_post
from ensemble_request.consts import URL
from ensemble_request.browse import post
from ..conftest import IBasicServerSetup


def test_non_bearer_token(basic_server_setup: IBasicServerSetup):
    """Tokens must start with 'Bearer '"""
    req_post(
        f"{URL}/browse/post/create",
        json={
            "heading": "My post",
            "text": "My text",
            "tags": [],
            "private": False,
            "anonymous": False,
        },
        headers={
            # Doesn't have bearer prefix
            "Authorization": basic_server_setup["token"]
        }
    )


def test_missing_token():
    """Token must be provided"""
    post.create(
        None,  # type: ignore
        "My post",
        "My text",
        [],
    )
