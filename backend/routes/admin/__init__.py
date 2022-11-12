"""
# Backend / Routes / Admin

Contains route definitions for functions used with administration
"""
import json
from flask import Blueprint, request
from .permissions import permissions
from .users import users
from .exam_mode import exam_mode
from backend.models.auth_config import AuthConfig
from backend.models.permissions import PermissionGroup, Permission
from backend.models.token import Token
from backend.models.queue import Queue
from backend.models.exam_mode import ExamMode
from backend.models.user import User
from backend.types.auth import IAuthInfo
from backend.types.admin import IIsFirstRun
from backend.util import http_errors
from backend.util.validators import assert_valid_str_field, assert_email_valid
from backend.util.auth_check import do_auth_check
from backend.types.admin import is_valid_request_type


admin = Blueprint('admin', 'admin')

admin.register_blueprint(permissions, url_prefix='/permissions')
admin.register_blueprint(users, url_prefix='/users')
admin.register_blueprint(exam_mode, url_prefix='/exam_mode')


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
    address: str = data["address"]
    request_type = str(data["request_type"]).lower()
    username_param: str = data["username_param"]
    password_param: str = data["password_param"]
    success_regex: str = data["success_regex"]
    username: str = data["username"]
    password: str = data["password"]
    email: str = data["email"]
    name_first: str = data["name_first"]
    name_last: str = data["name_last"]

    # Validate data
    assert_email_valid(email)
    assert_valid_str_field(name_first, "First name")
    assert_valid_str_field(name_last, "Last name")
    assert_valid_str_field(username, "Username")

    if not is_valid_request_type(request_type):
        raise http_errors.BadRequest(
            "Request type must be one of 'get', 'post', 'put', 'delete'"
        )

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

    # Base dictionary of permissions
    # all users should have no permissions by default
    base_permissions = {
        k: False for k in Permission
    }

    # Create permission groups
    admin = PermissionGroup.create(
        "Administrator",
        {
            # Admins have every permission
            k: True for k in Permission
        },
        immutable=True,
    )
    PermissionGroup.create(
        "Moderator",
        base_permissions | {
            k: True for k in [
                Permission.PostView,
                Permission.ViewPrivate,
                Permission.ViewAnonymousOP,
                Permission.PostCreate,
                Permission.PostComment,
                Permission.PostOverrideExam,
                Permission.ViewTaskboard,
                Permission.TaskboardDelegate,
                Permission.FollowQueue,
                Permission.ReportPosts,
                Permission.ClosePosts,
                Permission.DeletePosts,
                Permission.ViewReports,
                Permission.ViewAllUsers,
                Permission.CommentAccept,
            ]
        },
        immutable=False,
    )
    PermissionGroup.create(
        "User",
        base_permissions | {
            k: True for k in [
                Permission.PostView,
                Permission.PostCreate,
                Permission.PostComment,
                Permission.ReportPosts,
            ]
        },
        immutable=False,
    )

    # Initialise exam mode table and set exam mode to False
    ExamMode.initialise()

    # Create the main queue
    Queue.create(
        "Main queue",
        immutable=True,
    )

    # Create the answered queue
    Queue.create(
        "Answered queue",
        immutable=True
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
        "permissions": [
            {
                "permission_id": p.value,
                "value": user.permissions.can(p),
            } for p in Permission
        ],
    }


__all__ = [
    'admin',
]
