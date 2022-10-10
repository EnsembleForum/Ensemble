"""
# Tests / Integration / Request / User

Functions to request user-related routes
"""
from typing import cast
from .helpers import get
from backend.types.auth import JWT
from backend.types.identifiers import UserId
from backend.types.user import IUserProfile


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
        '/user/profile',
        {"user_id": user_id},
    ))
