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

    ## Body:
    * `users` (`list[IUserRegisterInfo]`): list of user info to add
    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.

    ## Returns:
    * `user_ids`: list of
          * `int`
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

    ### Returns:
    * `users`: `list`, containing dictionaries of:
          * `name_first`: `str`
          * `name_last`: `str`
          * `username`: `str`
          * `user_id`: `int`
    """
    return cast(IUserBasicInfoList, get(
        token,
        f'{URL}/all',
        {}
    ))
