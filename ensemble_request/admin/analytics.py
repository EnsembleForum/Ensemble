from typing import cast
from ..helpers import get
from ..consts import URL
from backend.types.auth import JWT
from backend.types.analytics import IAllStats

URL = f"{URL}/admin/analytics"


def get_analytics(token: JWT) -> IAllStats:
    """
    Returns a list of basic info about all forum users

    ## Permissions
    * `ViewAllUsers`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ### Returns
    * `users`: list of users, containing objects of
            * `name_first` (`str`): First name
            * `name_last` (`str`): Last name
            * `username` (`str`): Username
            * `user_id` (`int`): ID of the user
    """
    return cast(IAllStats, get(
        token,
        f'{URL}',
        {}
    ))
