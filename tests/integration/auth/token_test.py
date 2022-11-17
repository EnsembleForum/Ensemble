"""
# Tests / Integration / Auth / Token test

Tests for tokens
"""
import pytest
from requests import post as req_post
from backend.util.http_errors import Unauthorized
from ensemble_request.consts import URL
from ensemble_request.browse import post
from ..conftest import IBasicServerSetup


def test_non_bearer_token(basic_server_setup: IBasicServerSetup):
    """Tokens must start with 'Bearer '"""
    res = req_post(
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
    assert res.status_code == 403


def test_missing_token():
    """Token must be provided"""
    with pytest.raises(Unauthorized):
        post.create(
            None,  # type: ignore
            "My post",
            "My text",
            [],
        )
