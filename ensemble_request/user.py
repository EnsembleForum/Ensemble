"""
# Tests / Integration / Request / User

Functions to request user-related routes
"""
from typing import cast, Optional
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
    * `permission_group` (`str`): name of the user's permission group

    Note that this will eventually contain more properties such as pronouns and
    the like.

    ## Errors

    ### 400
    * Invalid user ID
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

    ## Errors

    ### 400
    * Invalid user ID
    * Empty first name

    ### 403
    * User does not have permission `EditProfile` if editing their own profile
    * User does not have permission `ManageUserProfile` if editing another
      user's profile
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

    ## Errors

    ### 400
    * Invalid user ID
    * Empty last name

    ### 403
    * User does not have permission `EditProfile` if editing their own profile
    * User does not have permission `ManageUserProfile` if editing another
      user's profile
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

    ## Errors

    ### 400
    * Invalid user ID
    * Invalid email

    ### 403
    * User does not have permission `EditProfile` if editing their own profile
    * User does not have permission `ManageUserProfile` if editing another
      user's profile
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
    pronouns: Optional[str],
) -> None:
    """
    ## PUT `/user/profile/edit_pronouns`

    Edits pronouns of a user.

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ### Params
    * `user_id` (`int`): user ID for user we're editing the profile of
    * `pronouns` (`Optional[str]`): user's new pronouns

    ## Errors

    ### 400
    * Invalid user ID
    * Empty pronouns (use `null` instead)

    ### 403
    * User does not have permission `EditProfile` if editing their own profile
    * User does not have permission `ManageUserProfile` if editing another
      user's profile
    """
    put(
        token,
        f'{URL}/profile/edit_pronouns',
        {
            "user_id": user_id,
            "pronouns": pronouns,
        },
    )
