"""
# Request / Debug

Functions that shadow server routes starting at /debug
"""
from typing import cast, NoReturn
from backend.types.debug import IEcho
from backend.types.admin import RequestType
from backend.types.auth import IAuthInfo
from .consts import URL
from .helpers import get, delete, post


URL = f"{URL}/debug"


def enabled() -> bool:
    """
    ## GET `debug/enabled`

    Returns whether debugging routes are enabled
    """
    return cast(bool, get(None, f"{URL}/enabled", {})["value"])


def echo(value: str) -> IEcho:
    """
    ## GET `debug/echo`

    Echo an input. This returns the given value, but also prints it to stdout
    and stderr on the server. Useful for debugging tests.

    ## Params
    * `value` (`str`): value to echo

    ## Returns
    Object containing:
    * `value`: the same value
    """
    return cast(IEcho, get(None, f"{URL}/echo", {"value": value}))


def clear() -> None:
    """
    ## DELETE `debug/clear`

    Clear the database.
    """
    delete(None, f"{URL}/clear", {})


def shutdown() -> None:
    """
    ## POST `debug/shutdown`

    Initiate a server shutdown.

    Currently this route is unused and unimplemented.
    """
    post(None, f"{URL}/shutdown", {})


def fail() -> NoReturn:
    """
    ## GET `debug/fail`

    Raise a 500 error. Used to test the custom error handling.
    """
    get(None, f"{URL}/fail", {})
    # If we reach this point then we have problems
    assert False


def unsafe_init(
    address: str,
    request_type: RequestType,
    username_param: str,
    password_param: str,
    success_regex: str,
    username: str,
    password: str,
    email: str,
    name_first: str,
    name_last: str,
) -> IAuthInfo:
    """
    ## GET `/debug/unsafe_init`

    Initialise the forum.

    This behaves very similarly to `/admin/init` (which should be used
    normally), but skips certain critical auth checks in the interest of
    performance.

    It is used during testing to increase the performance of tests massively,
    but should NEVER, EVER, EVER be used in a production environment as it
    could result in a broken server.

    * Sets up the authentication system
    * Creates permission groups "Admin", "Moderator", "User"
    * Registers a first user as an admin

    ## Body
    * `address` (`str`): address to query for auth
    * `request_type` (`str`): type of request (eg post, get)
    * `username_param` (`str`): parameter to use for username in request for
      auth
    * `password_param` (`str`): parameter to use for password in request for
      auth
    * `success_regex` (`str`): regular expression to check for auth success
    * `username` (`str`): username for first user
    * `password` (`str`): password to use with first user
    * `email` (`str`): email for first user
    * `name_first` (`str`): first name for first user
    * `name_last` (`str`): last name for first user

    ## Returns
    Object containing:
    * `user_id`: `UserId`
    * `token`: `JWT`
    * `permissions`: List of objects, each containing:
            * `permission_id` (`int`): ID of the permission
            * `value` (`bool`): whether the permission is granted
    """
    return cast(IAuthInfo, post(None, f"{URL}/unsafe_init", {
        "address": address,
        "request_type": request_type,
        "username_param": username_param,
        "password_param": password_param,
        "success_regex": success_regex,
        "username": username,
        "password": password,
        "email": email,
        "name_first": name_first,
        "name_last": name_last,
    }))


def unsafe_login(username: str) -> IAuthInfo:
    """
    ## POST `/debug/unsafe_login`

    Log in a user that has been registered

    This behaves very similarly to `/auth/login` (which should be used
    normally), but skips certain critical checks in the interest of
    performance.

    It is used during testing to increase the performance of tests massively,
    but should NEVER, EVER, EVER be used in a production environment as it
    removes all security.

    ## Body
    * `username` (`str`): the user's username

    ## Returns
    Object containing:
    * `user_id` (`int`): ID of user who logged in
    * `token` (`str`): a new token belonging to the user who logged in. This
      should be given as a header for most other requests.
    * `permissions`: List of objects, each containing:
            * `permission_id` (`int`): ID of the permission
            * `value` (`bool`): whether the permission is granted
    """
    return cast(IAuthInfo, post(
        None,
        f"{URL}/unsafe_login",
        {
            "username": username,
        }
    ))
