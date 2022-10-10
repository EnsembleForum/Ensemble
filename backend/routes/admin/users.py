import json
from flask import Blueprint, request
from backend.types.user import (
    IUserIdList,
    IUserBasicInfoList,
    IUserProfile,
    IUserRegisterInfo,
)
from backend.types.identifiers import PermissionGroupId
from backend.util.validators import assert_email_valid, assert_name_valid
from backend.util import http_errors
from backend.util.tokens import uses_token
from backend.models.user import User
from backend.models.permissions import PermissionGroup, Permission


users = Blueprint('users', 'users')


@users.post('/register')
@uses_token
def register(user: User, *_) -> IUserIdList:
    """
    Register a collection of users

    ## Body:
    * `users` (`list[IUserRegisterInfo]`): list of user info to add
    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.

    ## Returns:
    * `user_ids`: list of
          * `int`

    ## TODO:
    * Improve error messages to be more helpful to user
    """
    # Check that the user has permission to create users
    if not user.permissions.can(Permission.AddUsers):
        raise http_errors.Forbidden("You don't have permission to add users")

    data = json.loads(request.data)
    users: list[IUserRegisterInfo] = data["users"]
    group: PermissionGroupId = data["group_id"]

    # Check for duplicates in sign-up list
    unique_usernames = set(map(lambda u: u['username'].lower(), users))
    if len(unique_usernames) < len(users):
        raise http_errors.BadRequest("Duplicate usernames are not allowed")
    unique_emails = set(map(lambda u: u['email'].lower(), users))
    if len(unique_emails) < len(users):
        raise http_errors.BadRequest("Duplicate emails are not allowed")

    # Make sure each email and username isn't present already, and that
    # username is alphanumeric
    for username in unique_usernames:
        assert_name_valid(username, "Username")
        if not username.isalnum():
            raise http_errors.BadRequest(
                f"Username {username} is not alphanumeric"
            )
        try:
            User.from_username(username)
        except http_errors.BadRequest:
            pass
        else:
            raise http_errors.BadRequest(f"Username {username} already exists")
    for email in unique_emails:
        assert_email_valid(email)
        try:
            User.from_email(email)
        except http_errors.BadRequest:
            pass
        else:
            raise http_errors.BadRequest(f"Email {email} already exists")

    # Make sure names are not empty
    for u in users:
        assert_name_valid(u['name_first'], "First name")
        assert_name_valid(u['name_last'], "Last name")

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
@uses_token
def all(user: User, *_) -> IUserBasicInfoList:
    """
    Returns a list of basic info about all forum users

    ### Returns:
    * `users`: `list`, containing dictionaries of:
          * `name_first`: `str`
          * `name_last`: `str`
          * `username`: `str`
          * `user_id`: `int`
    """
    # Check that the user has permission
    if not user.permissions.can(Permission.ViewAllUsers):
        raise http_errors.Forbidden(
            "You don't have permission to view all users"
        )
    return {
        "users": list(map(lambda u: u.basic_info(), User.all()))
    }
