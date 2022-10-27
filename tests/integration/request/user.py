"""
# Tests / Integration / Request / User

Functions to request user-related routes
"""
from typing import cast
from .consts import URL
from .helpers import get, put
from backend.types.auth import JWT
from backend.types.identifiers import UserId
from backend.types.user import IUserProfile

URL = f"{URL}/user"


def profile(token: JWT, user_id: UserId) -> IUserProfile:
    """
    Returns detailed info about the

    ### Args:
    * `token` (`JWT`): token
    * `user_id` (`UserId`): user ID for user we're viewing the profile of

    ### Returns:
    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `email`: `str`
    * `user_id`: `int`

    Note that this will eventually contain more properties such as pronouns and
    the like
    """
    return cast(IUserProfile, get(
        token,
        f'{URL}/profile',
        {"user_id": user_id},
    ))


def profile_edit_first(token: JWT, user_id: UserId, new_name: str) -> IUserProfile:
    return cast(IUserProfile, put(
        token,
        f'{URL}/profile/edit_name_first',
        {
            "user_id": user_id,
            "new_name": new_name,
        }
        ,
    ))


def profile_edit_last(token: JWT, user_id: UserId, new_name: str) -> IUserProfile:
    return cast(IUserProfile, put(
        token,
        f'{URL}/profile/edit_name_last',
        {
            "user_id": user_id,
            "new_name": new_name,
        },
    ))
