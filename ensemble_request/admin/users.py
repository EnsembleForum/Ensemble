from typing import cast
from ..helpers import post, get
from ..consts import URL
from backend.types.auth import JWT
from backend.types.user import (
    IUserRegisterInfo,
    IUserIdList,
    IUserBasicInfoList,
)
from backend.types.identifiers import PermissionGroupId

URL = f"{URL}/admin/users"


def register(
    token: JWT,
    users: list[IUserRegisterInfo],
    group_id: PermissionGroupId
) -> IUserIdList:
    """
    Register a collection of users

    ## Permissions
    * `AddUsers`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `users`: list of user info to add. Each user must be an object of:
            * `name_first` (`str`): First name
            * `name_last` (`str`): Last name
            * `username` (`str`): Username (which they will log in using)
            * `email` (`str`): Email address through which they will receive
              notifications

    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.

    ## Returns
    * `user_ids`: list of
          * `int`: ID for the user
    """
    return cast(IUserIdList, post(
        token,
        f'{URL}/register',
        {
            'users': users,
            'group_id': group_id
        }
    ))


def all(token: JWT) -> IUserBasicInfoList:
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
    return cast(IUserBasicInfoList, get(
        token,
        f'{URL}/all',
        {}
    ))
