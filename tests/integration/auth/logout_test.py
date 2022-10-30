"""
# Tests / Integration / Auth / Logout test

Tests for logging out

* Token invalidated
* No errors for invalid tokens
"""
import pytest
from backend.util import http_errors
from backend.types.auth import JWT
from ..conftest import IAllUsers
from ensemble_request.auth import logout
from ensemble_request.user import profile


def test_token_invalidated(all_users: IAllUsers):
    """Does the token get invalidated when we log out?"""
    logout(all_users['admins'][0]['token'])
    with pytest.raises(http_errors.Forbidden):
        profile(
            all_users['admins'][0]['token'],
            all_users['admins'][0]['user_id'],
        )


def test_no_error_for_invalid_token():
    """Do we get no errors if the token is invalid?"""
    logout(JWT('not.a.token'))
