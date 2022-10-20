"""
# Tests / Integration / Auth / Login test

Tests for logging in

* Fails with incorrect username/password
* Fails with correct username/password but not in database
* Succeeds with correct input
* Different logins from same user get different tokens but same user_id
* Already has token
"""
import pytest
from backend.util import http_errors
from tests.integration.conftest import IBasicServerSetup
from request.auth import login, post, URL, JWT


def test_fails_incorrect_username(basic_server_setup: IBasicServerSetup):
    """Do we fail to log in if we have an incorrect username?"""
    with pytest.raises(http_errors.Forbidden):
        login(
            'not a user',
            'admin1',
        )


def test_fails_incorrect_password(basic_server_setup: IBasicServerSetup):
    """Do we fail to log in if we have an incorrect password?"""
    with pytest.raises(http_errors.Forbidden):
        login(
            'admin1',
            'not a password',
        )


def test_fails_not_registered(basic_server_setup: IBasicServerSetup):
    """Do we fail to log in if we have a correct username and password, but
    we haven't been added as an ensemble user?
    """
    with pytest.raises(http_errors.BadRequest):
        login('admin2', 'admin2')


def test_success(basic_server_setup: IBasicServerSetup):
    """Can we login if we give the correct details of a registered user?"""
    res = login(
        'admin1',
        'admin1',
    )
    assert isinstance(res['token'], str)
    assert isinstance(res['user_id'], int)


def test_different_tokens(basic_server_setup: IBasicServerSetup):
    """Do we get different tokens but the same user_id when we log in twice
    with the same user?
    """
    res1 = login(
        'admin1',
        'admin1',
    )
    res2 = login(
        'admin1',
        'admin1',
    )
    assert res1['user_id'] == res2['user_id']
    assert res1['token'] != res2['token']


def test_fails_already_logged_in(basic_server_setup: IBasicServerSetup):
    """Do we fail to log in if we provide a token when logging in?"""
    with pytest.raises(http_errors.BadRequest):
        post(
            basic_server_setup['token'],
            f"{URL}/login",
            {
                "username": "admin1",
                "password": "admin1",
            }
        )


def test_already_logged_in_invalid_token(
    basic_server_setup: IBasicServerSetup
):
    """Can we log in if we provide an invalid token?"""
    ret = post(
        JWT(basic_server_setup['token'] + 'invalid'),
        f"{URL}/login",
        {
            "username": "admin1",
            "password": "admin1",
        }
    )
    assert ret["token"] != basic_server_setup['token']
