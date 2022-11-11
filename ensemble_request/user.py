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
    ## GET `/user/profile`

    Returns detailed info about a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

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


def profile_edit_first(token: JWT, user_id: UserId, new_name: str) \
        -> IUserProfile:
    """
    ## PUT `/user/profile`

    Edits first name of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're viewing the profile of
    * `new_name` (`str`): user's new first name

    ### Returns
    * `name_first` (`str`): the user's first name
    * `name_last` (`str`): the user's last name
    * `username` (`str`): the user's username
    * `email` (`str`): the user's email address
    * `user_id` (`int`): the user's ID

    """
    return cast(IUserProfile, put(
        token,
        f'{URL}/profile/edit_name_first',
        {
            "user_id": user_id,
            "new_name": new_name,
        },
    ))


def profile_edit_last(token: JWT, user_id: UserId, new_name: str) \
        -> IUserProfile:
    """
    ## PUT `/user/profile`

    Edits last name of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're viewing the profile of
    * `new_name` (`str`): user's new last name

    ### Returns
    * `name_first` (`str`): the user's first name
    * `name_last` (`str`): the user's last name
    * `username` (`str`): the user's username
    * `email` (`str`): the user's email address
    * `user_id` (`int`): the user's ID

    """
    return cast(IUserProfile, put(
        token,
        f'{URL}/profile/edit_name_last',
        {
            "user_id": user_id,
            "new_name": new_name,
        },
    ))
