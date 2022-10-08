from typing import cast
from ..helpers import post, get
from ..consts import URL
from backend.types.user import (
    IUserRegisterInfo,
    IUserIdList,
    IUserBasicInfoList,
)
from backend.types.identifiers import PermissionGroupId

URL = f"{URL}/admin/users"


def register(
    users: list[IUserRegisterInfo],
    group_id: PermissionGroupId
) -> IUserIdList:
    """
    Register a collection of users

    ## Body:
    * `users` (`list[IUserRegisterInfo]`): list of user info to add
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


def all() -> IUserBasicInfoList:
    """
    Returns a list of basic info about all forum users

    ### Returns:
    * `IUserBasicInfoList`: list of user info
    """
    return cast(IUserBasicInfoList, get(
        f'{URL}/all',
        {}
    ))
