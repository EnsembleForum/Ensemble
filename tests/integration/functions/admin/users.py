from typing import cast
from ..helpers import post
from ..consts import URL
from backend.types.user import IUserBasicDetails, IUserIdList
from backend.types.identifiers import PermissionGroupId

URL = f"{URL}/admin/users"


def register(
    users: list[IUserBasicDetails],
    group_id: PermissionGroupId
) -> IUserIdList:
    """
    Register a collection of users

    ## Body:
    * `users` (`list[IUserBasicDetails]`): list of user info to add
    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.

    ## Returns:
    * `IUserIdList`: list of new user IDs
    """
    return cast(IUserIdList, post(
        f'{URL}/register',
        {
            'users': users,
            'group_id': group_id
        }
    ))
