"""
# Tests / Integration / Auth / Logout test

Tests for logging out

* Token invalidated
* No errors for invalid tokens
"""
import pytest
from backend.util import http_errors
from backend.types.auth import JWT
from ..conftest import IBasicServerSetup
from ensemble_request.auth import logout
from ensemble_request.user import profile


def test_token_invalidated(basic_server_setup: IBasicServerSetup):
    """Does the token get invalidated when we log out?"""
    logout(basic_server_setup['token'])
    with pytest.raises(http_errors.Forbidden):
        profile(
            basic_server_setup['token'],
            basic_server_setup['user_id'],
        )


def test_no_error_for_invalid_token():
    """Do we get no errors if the token is invalid?"""
    logout(JWT('not.a.token'))
