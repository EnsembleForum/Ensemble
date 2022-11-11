"""
# Tests / Integration / Request / Admin
"""
from backend.types.admin import IIsFirstRun, RequestType
from backend.types.auth import IAuthInfo
from typing import cast
from ..consts import URL
from ..helpers import get, post
from . import permissions
from . import users

__all__ = [
    'permissions',
    'users',
    'is_first_run',
    'init',
]


URL = f"{URL}/admin"


def is_first_run() -> IIsFirstRun:
    """
    ## GET `/admin/is_first_run`

    Returns whether the datastore is empty

    ## Returns:
    Object containing:
    * `value` (`bool`): `True` if the server hasn't been initialised
    """
    return cast(IIsFirstRun, get(None, f"{URL}/is_first_run", {}))


def init(
    address: str,
    request_type: RequestType,
    username_param: str,
    password_param: str,
    success_regex: str,
    username: str,
    password: str,
    email: str,
    pronoun: str,
    name_first: str,
    name_last: str,
) -> IAuthInfo:
    """
    ## GET `/admin/init`

    Initialise the forum.

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
    return cast(IAuthInfo, post(None, f"{URL}/init", {
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
