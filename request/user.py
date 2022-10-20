"""
# Tests / Integration / Request / User

Functions to request user-related routes
"""
from typing import cast
from .consts import URL
from .helpers import get
from backend.types.auth import JWT
from backend.types.identifiers import UserId
from backend.types.user import IUserProfile

URL = f"{URL}/user"


def profile(token: JWT, user_id: UserId) -> IUserProfile:
    """
    ## GET `/user/profile`

    Returns detailed info about a user.

    ## Header
    * `token` (`str`): JWT of the user performing the action

    ### Params
    * `user_id` (`int`): user ID for user we're viewing the profile of

    ### Returns
    * `name_first` (`str`): the user's first name
    * `name_last` (`str`): the user's last name
    * `username` (`str`): the user's username
    * `email` (`str`): the user's email address
    * `user_id` (`int`): the user's ID

    Note that this will eventually contain more properties such as pronouns and
    the like.
    """
    return cast(IUserProfile, get(
        token,
        f'{URL}/profile',
        {"user_id": user_id},
    ))
