import json
from flask import Blueprint, request
from backend.types.user import (
    IUserIdList,
    IUserBasicInfoList,
    IUserProfile,
    IUserRegisterInfo,
)
from backend.types.identifiers import PermissionGroupId
from backend.util import http_errors
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

    # Check for duplicates in sign-up list
    # TODO: Give more helpful error info (eg which users cause the problem)
    unique_usernames = set(map(lambda u: u['username'], users))
    if len(unique_usernames) < len(users):
        raise http_errors.BadRequest("Duplicate usernames are not allowed")
    unique_emails = set(map(lambda u: u['email'], users))
    if len(unique_emails) < len(users):
        raise http_errors.BadRequest("Duplicate emails are not allowed")

    def new_user(u: IUserRegisterInfo):
        return User.create(
            u['username'],
            u['name_first'],
            u['name_last'],
            u['email'],
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
    return {
        "users": list(map(lambda u: u.basic_info(), User.all()))
    }


@users.get('/profile')
def profile() -> IUserProfile:
    """
    Returns detailed info about a user's profile

    ### Returns:
    * `IUserProfile`: list of user info
    """
    data = json.loads(request.data)
    user_id = data["user_id"]
    return User(user_id).profile()
