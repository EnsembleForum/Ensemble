"""
# Backend / Routes / Admin

Contains route definitions for functions used with administration
"""
import json
from flask import Blueprint, request
from .permissions import permissions
from .users import users
from backend.models.auth_config import AuthConfig
from backend.models.permissions import PermissionGroup, Permission
from backend.models.token import Token
from backend.models.user import User
from backend.types.auth import IAuthInfo
from backend.types.admin import IIsFirstRun
from backend.util import http_errors
from backend.util.validators import assert_name_valid, assert_email_valid
from backend.util.auth_check import do_auth_check


admin = Blueprint('admin', 'admin')

admin.register_blueprint(permissions, url_prefix='/permissions')
admin.register_blueprint(users, url_prefix='/users')


@admin.get('/is_first_run')
def is_first_run() -> IIsFirstRun:
    """
    Returns whether the datastore is empty

    ## Returns:
    * { value: bool }
    """
    return {"value": not AuthConfig.exists()}


@admin.post('/init')
def init() -> IAuthInfo:
    """
    Initialise the forum.

    * Sets up the authentication system
    * Creates permission groups "Admin", "Moderator", "User"
    * Registers a first user as an admin

    ## Body:
    * `address` (`str`): address to query for auth
    * `request_type` (`str`): type of request (eg post, get)
    * `username_param` (`str`): parameter to use for username in request for
      auth
    * `password_param` (`str`): parameter to use for password in request for
      auth
    * `success_regex` (`str`): regular expression to check for auth success
    * `username` (`str`): username for first user
    * `password` (`str`): password to use with first user
    * `email` (`str`): email for first user
    * `name_first` (`str`): first name for first user
    * `name_last` (`str`): last name for first user

    ## Returns:
    * `user_id`: `UserId`
    * `token`: `JWT`
    """
    if AuthConfig.exists():
        raise http_errors.Forbidden(
            "Ensemble Forum has already been set up, so this route has been "
            "disabled."
        )
    data = json.loads(request.data.decode('utf-8'))
    address = data["address"]
    request_type = data["request_type"]
    username_param = data["username_param"]
    password_param = data["password_param"]
    success_regex = data["success_regex"]
    username = data["username"]
    password = data["password"]
    email = data["email"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    # Validate data
    assert_email_valid(email)
    assert_name_valid(name_first, "First name")
    assert_name_valid(name_last, "Last name")
    assert_name_valid(username, "Username")

    # Make sure we can log in with the auth system
    if not do_auth_check(
        address,
        request_type,
        username_param,
        password_param,
        success_regex,
        username,
        password,
    ):
        raise http_errors.BadRequest(
            "Authentication request failed. This either means that your "
            "username or password is incorrect, or that the request "
            "configuration is set incorrectly."
        )

    # If we give an incorrect password and it still works, then something has
    # gone terribly wrong
    if do_auth_check(
        address,
        request_type,
        username_param,
        password_param,
        success_regex,
        username,
        password + "now_incorrect",
    ):
        raise http_errors.BadRequest(
            "Authentication request succeeded in failure test. This either "
            "means that your success regular expression is matching cases "
            "where login is failing, or that your authentication system is "
            "insecure (unlikely)."
        )

    # Set up authentication system
    AuthConfig.create(
        address,
        request_type,
        username_param,
        password_param,
        success_regex
    )

    # Create permission groups
    admin = PermissionGroup.create(
        "Administrator",
        {
            Permission.View: True,
            Permission.ViewPrivate: True,
            Permission.ViewAnonymousOP: True,
            Permission.Post: True,
            Permission.Answer: True,
            Permission.PostOverrideExam: True,
            Permission.ViewTaskboard: True,
            Permission.Delegate: True,
            Permission.FollowQueue: True,
            Permission.ReportPosts: True,
            Permission.ClosePosts: True,
            Permission.DeletePosts: True,
            Permission.ViewReports: True,
            Permission.ManageUserPermissions: True,
            Permission.AddUsers: True,
            Permission.RemoveUsers: True,
            Permission.ViewAllUsers: True,
            Permission.ManageAuthConfig: True,
            Permission.ManagePermissionGroups: True,
        }
    )
    PermissionGroup.create(
        "Moderator",
        {
            Permission.View: True,
            Permission.ViewPrivate: True,
            Permission.ViewAnonymousOP: True,
            Permission.Post: True,
            Permission.Answer: True,
            Permission.PostOverrideExam: True,
            Permission.ViewTaskboard: True,
            Permission.Delegate: True,
            Permission.FollowQueue: True,
            Permission.ReportPosts: True,
            Permission.ClosePosts: True,
            Permission.DeletePosts: True,
            Permission.ViewReports: True,
            Permission.ManageUserPermissions: False,
            Permission.AddUsers: False,
            Permission.RemoveUsers: False,
            Permission.ViewAllUsers: True,
            Permission.ManageAuthConfig: False,
            Permission.ManagePermissionGroups: False,
        }
    )
    PermissionGroup.create(
        "User",
        {
            Permission.View: True,
            Permission.ViewPrivate: False,
            Permission.ViewAnonymousOP: False,
            Permission.Post: True,
            Permission.Answer: True,
            Permission.PostOverrideExam: False,
            Permission.ViewTaskboard: False,
            Permission.Delegate: False,
            Permission.FollowQueue: False,
            Permission.ReportPosts: True,
            Permission.ClosePosts: False,
            Permission.DeletePosts: False,
            Permission.ViewReports: False,
            Permission.ManageUserPermissions: False,
            Permission.AddUsers: False,
            Permission.RemoveUsers: False,
            Permission.ViewAllUsers: False,
            Permission.ManageAuthConfig: False,
            Permission.ManagePermissionGroups: False,
        }
    )

    # Register first user
    user = User.create(
        username,
        name_first,
        name_last,
        email,
        admin,
    )

    # Return user information
    return {
        "user_id": user.id,
        "token": Token.create(user).encode(),
    }


__all__ = [
    'admin',
]
