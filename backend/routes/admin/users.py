import json
from flask import Blueprint, request
from backend.types.user import (
    IUserIdList,
    IUserBasicInfoList,
    IUserProfile,
    IUserRegisterInfo,
)
from backend.types.identifiers import PermissionGroupId
from backend.models.user import User
from backend.models.permissions import PermissionGroup


users = Blueprint('users', 'users')


@users.post('/register')
def register() -> IUserIdList:
    """
    Register a collection of users

    ## Body:
    * `users` (`list[IUserRegisterInfo]`): list of user info to add
    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.

    ## Returns:
    * `IUserIdList`: list of new user IDs
    """
    # NOTE: currently not handling things properly, this is entirely to test
    # the database and will need some improvement
    data = json.loads(request.data)
    users: list[IUserRegisterInfo] = data["users"]
    group: PermissionGroupId = data["group_id"]

    def new_user(u: IUserRegisterInfo):
        return User.create(
            u['name_first'],
            u['name_last'],
            PermissionGroup(group),
        ).id
    return {
        "user_ids": list(map(new_user, users))
    }


@users.get('/all')
def all() -> IUserBasicInfoList:
    """
    Returns a list of basic info about all forum users

    ### Returns:
    * `IUserBasicInfoList`: list of user info
    """


@users.get('/profile')
def profile() -> IUserProfile:
    """
    Returns detailed info about a user's profile

    ### Returns:
    * `IUserProfile`: list of user info
    """
