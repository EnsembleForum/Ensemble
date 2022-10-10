"""
# Tests / Integration / Request / Auth

Helper functions for requesting auth code
"""
from typing import cast
from backend.types.auth import IAuthInfo, JWT
from .consts import URL
from .helpers import post


URL = f"{URL}/auth"


def login(username: str, password: str) -> IAuthInfo:
    """
    Log in a user that has been registered

    ## Body:
    * `username` (`str`)
    * `password` (`str`)

    ## Returns:
    * `user_id`: `UserId`
    * `token`: `JWT`
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
    Log out a logged in user
    """
    post(token, f"{URL}/logout", {})
