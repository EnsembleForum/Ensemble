"""
# Tests / Integration / Request / Auth

Helper functions for requesting auth code
"""
from typing import cast
from backend.types.auth import IAuthInfo
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
        f"{URL}/login",
        {
            "username": username,
            "password": password,
        }
    ))


def logout() -> None:
    """
    Log out a logged in user
    """
    post(f"{URL}/logout", {})
