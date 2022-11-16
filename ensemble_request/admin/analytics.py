from typing import cast
from ..helpers import get
from ..consts import URL
from backend.types.auth import JWT
from backend.types.analytics import IAllStats

URL = f"{URL}/admin/analytics"


def get_analytics(token: JWT) -> IAllStats:
    """
    # GET `/admin/analytics`

    Returns the analytics about the activity on the forum

    ## Permissions
    * `ViewAnalytics`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ### Returns
    Object containing
    * `total_posts` (`int`)
    * `total_comments` (`int`)
    * `total_replies` (`int`)
    * `all_users`: dictionary containing
        * top_posters: list[{"user_id": int, "count": int}]
        * top_commenters:  list[{"user_id": int, "count": int}]
        * top_repliers: list[{"user_id": int, "count": int}]
        * top_me_too:  list[{"user_id": int, "count": int}]
        * top_thanks:  list[{"user_id": int, "count": int}]
    * `groups`: list of dictionaries containing
        * permission_group_id: PermissionGroupId
        * permission_group_name: str
        * stats: dictionary containing
            * top_posters: list[{"user_id": int, "count": int}]
            * top_commenters:  list[{"user_id": int, "count": int}]
            * top_repliers: list[{"user_id": int, "count": int}]
            * top_me_too:  list[{"user_id": int, "count": int}]
            * top_thanks:  list[{"user_id": int, "count": int}]
    """
    return cast(IAllStats, get(
        token,
        f'{URL}',
        {}
    ))
