"""
# Tests / Integration / Admin / Setup test

Tests for server setup

## /is_first_run

* first run empty
* not first run not empty

## /init

* Server already set up
* Can't connect to auth server
* User and password failed to authenticate
* Incorrect username/password shouldn't authenticate
* Email not valid
* name_first empty
* name_last empty
* User gets registered
* Permission groups get created: #  TODO
"""
import pytest
from backend.util import http_errors
from ensemble_request.admin import is_first_run, init
from ensemble_request.auth import login
from mock.auth import AUTH_URL


@pytest.mark.core
def test_first_run_empty():
    """
    When we clear the server, does is_first_run return True when the server
    isn't set up?
    """
    assert is_first_run()["value"]


def test_not_first_run_not_empty():
    """
    When we set up the server, does is_first_run stop returning True?
    """
    init(
        address=f"{AUTH_URL}/login",
        request_type="get",
        username_param="username",
        password_param="password",
        success_regex="true",
        username="admin1",
        password="admin1",
        email="admin@example.com",
        name_first="Dee",
        name_last="Snuts",
    )
    assert not is_first_run()["value"]


def test_init_server_already_set_up():
    """
    If we try to set up an already setup server, do we get a 403 error?
    """
    init(
        address=f"{AUTH_URL}/login",
        request_type="get",
        username_param="username",
        password_param="password",
        success_regex="true",
        username="admin1",
        password="admin1",
        email="admin@example.com",
        name_first="Dee",
        name_last="Snuts",
    )
    with pytest.raises(http_errors.Forbidden):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


def test_cant_connect_to_auth_server():
    """
    Do we get a 400 error when we give an invalid auth server?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address="http://localhost:6969/login",  # Bad server
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


def test_invalid_route_auth_server():
    """
    Do we get a 400 error when we give an invalid URL to the correct server?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/not_login",  # Bad URL
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


@pytest.mark.parametrize(
    'req_type',
    [
        'post',
        'put',
        'delete',
    ]
)
def test_incorrect_request_type_auth_server(req_type):
    """
    Do we get a 400 error when we give an invalid URL to the correct server?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type=req_type,
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


def test_invalid_regex():
    """
    Do we get a 400 error when we give an invalid regex for the success_regex?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="*",  # Bad regex, fails to compile
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


def test_username_password_failed_to_authenticate_username():
    """
    Do we get a 400 error if an invalid username and password are given?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1_no",  # Bad username
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1_no",  # Bad password
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


def test_incorrect_username_or_password_doesnt_authenticate():
    """
    Do we get a 400 error if an invalid username and password are given?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex=r"[\s\S]",  # Match everything
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="Snuts",
        )


def test_init_email_not_valid():
    """
    Do we get a 400 error if an invalid email is given
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin_example.com",  # Invalid email
            name_first="Dee",
            name_last="Snuts",
        )


def test_first_name_empty():
    """
    If first_name is empty, do we get a 400 error?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="",  # Empty
            name_last="Snuts",
        )


def test_last_name_empty():
    """
    If last_name is empty, do we get a 400 error?
    """
    with pytest.raises(http_errors.BadRequest):
        init(
            address=f"{AUTH_URL}/login",
            request_type="get",
            username_param="username",
            password_param="password",
            success_regex="true",
            username="admin1",
            password="admin1",
            email="admin@example.com",
            name_first="Dee",
            name_last="",  # Empty
        )


@pytest.mark.core
def test_init_user_created():
    """
    When we initialise the server, does a user get created?
    """
    init(
        address=f"{AUTH_URL}/login",
        request_type="get",
        username_param="username",
        password_param="password",
        success_regex="true",
        username="admin1",
        password="admin1",
        email="admin@example.com",
        name_first="Dee",
        name_last="Snuts",
    )
    # Test we can log in with their account
    login("admin1", "admin1")


def test_login_with_no_config():
    """
    Do we get an error if we try to log in when there's no auth configuration?
    """
    with pytest.raises(http_errors.BadRequest):
        login("admin1", "admin1")
