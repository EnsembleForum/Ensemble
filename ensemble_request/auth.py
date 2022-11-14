"""
# Request / Auth

Helper functions for requesting auth code
"""
from typing import cast
from backend.types.auth import IAuthInfo, IUserPermissions, JWT
from .consts import URL
from .helpers import post, get


URL = f"{URL}/auth"


def login(username: str, password: str) -> IAuthInfo:
    """
    ## POST `/auth/login`

    Log in a user that has been registered

    ## Body
    * `username` (`str`): the user's username
    * `password` (`str`): the user's password

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
        f"{URL}/login",
        {
            "username": username,
            "password": password,
        }
    ))


def logout(token: JWT) -> None:
    """
    ## POST `/auth/logout`

    Log out a logged in user, invalidating their token so it can no-longer be
    used.

    ## Header
    * `Authorization` (`str`): JWT of the user
    """
    post(token, f"{URL}/logout", {})


def permissions(token: JWT) -> IUserPermissions:
    """
    ## GET `/auth/permissions`

    Returns the currently available permissions for a user. This should be
    called frequently to ensure that the frontend doesn't display content that
    shouldn't be visible to the token bearer.

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Returns
    * `permissions`: List of objects, each containing:
            * `permission_id` (`int`): ID of the permission
            * `value` (`bool`): whether the permission is granted
    """
    return cast(IUserPermissions, get(token, f'{URL}/permissions', {}))
