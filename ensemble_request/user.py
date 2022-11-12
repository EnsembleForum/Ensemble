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


def profile_edit_name_first(
    token: JWT,
    user_id: UserId,
    name_first: str,
) -> None:
    """
    ## PUT `/user/profile/edit_name_first`

    Edits first name of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're editing the profile of
    * `name_first` (`str`): user's new first name
    """
    put(
        token,
        f'{URL}/profile/edit_name_first',
        {
            "user_id": user_id,
            "name_first": name_first,
        },
    )


def profile_edit_name_last(
    token: JWT,
    user_id: UserId,
    name_last: str,
) -> None:
    """
    ## PUT `/user/profile/edit_name_last`

    Edits last name of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're editing the profile of
    * `name_last` (`str`): user's new last name
    """
    put(
        token,
        f'{URL}/profile/edit_name_last',
        {
            "user_id": user_id,
            "name_last": name_last,
        },
    )


def profile_edit_email(
    token: JWT,
    user_id: UserId,
    email: str,
) -> None:
    """
    ## PUT `/user/profile/edit_email`

    Edits email of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're editing the profile of
    * `email` (`str`): user's new email
    """
    put(
        token,
        f'{URL}/profile/edit_email',
        {
            "user_id": user_id,
            "email": email,
        },
    )


def profile_edit_pronouns(
    token: JWT,
    user_id: UserId,
    pronouns: str,
) -> None:
    """
    ## PUT `/user/profile/edit_pronouns`

    Edits pronouns of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're editing the profile of
    * `pronouns` (`str`): user's new pronouns
    """
    put(
        token,
        f'{URL}/profile/edit_pronouns',
        {
            "user_id": user_id,
            "pronouns": pronouns,
        },
    )
