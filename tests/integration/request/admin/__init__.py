"""
# Tests / Integration / Request / Admin
"""
from backend.types.admin import IIsFirstRun
from backend.types.auth import IAuthInfo
from typing import cast, Literal
from ..consts import URL
from ..helpers import get, post

URL = f"{URL}/admin"


def is_first_run() -> IIsFirstRun:
    """
    Returns whether the datastore is empty

    ## Returns:
    * { value: bool }
    """
    return cast(IIsFirstRun, get(f"{URL}/is_first_run", {}))


def init(
    address: str,
    request_type: Literal['get', 'post'],
    username_param: str,
    password_param: str,
    success_regex: str,
    username: str,
    password: str,
    email: str,
    name_first: str,
    name_last: str,
) -> IAuthInfo:
    """"
    Initialise the forum.

    * Sets up the authentication system
    * Creates permission groups "Admin", "Moderator", "User"
    * Registers a first user as an admin

    ## Body:
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

    ## Returns:
    * `user_id`: `UserId`
    * `token`: `JWT`
    """
    return cast(IAuthInfo, post(f"{URL}/init", {
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
