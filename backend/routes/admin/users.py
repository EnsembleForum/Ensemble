import json
from flask import Blueprint, request
from backend.types.user import (
    IUserIdList,
    IUserBasicInfoList,
    IUserRegisterInfo,
)
from backend.types.identifiers import PermissionGroupId
from backend.models import User, PermissionGroup, Permission
from backend.util.validators import assert_email_valid, assert_valid_str_field
from backend.util import http_errors
from backend.util.tokens import uses_token


users = Blueprint('users', 'users')


@users.post('/register')
@uses_token
def register(user: User, *_) -> IUserIdList:
    # TODO: Improve error messages to be more helpful to user
    user.permissions.assert_can(Permission.AddUsers)

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
        assert_valid_str_field(username, "Username")
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
        assert_valid_str_field(u['name_first'], "First name")
        assert_valid_str_field(u['name_last'], "Last name")

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
    user.permissions.assert_can(Permission.ViewAllUsers)
    return {
        "users": list(map(lambda u: u.basic_info(), User.all()))
    }
