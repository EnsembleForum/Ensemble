"""
# Backend / Util / Setup

Code used to initialise the server
"""
from resources import consts
from backend.types.auth import IAuthInfo
from backend.models.auth_config import AuthConfig
from backend.models.permissions import PermissionGroup, Permission
from backend.models.token import Token
from backend.models.post_queue import Queue
from backend.models.exam_mode import ExamMode
from backend.models.user import User
from backend.util import http_errors
from backend.util.validators import assert_valid_str_field, assert_email_valid
from backend.util.auth_check import do_auth_check
from backend.types.admin import is_valid_request_type


def init(
    address: str,
    request_type: str,
    username_param: str,
    password_param: str,
    success_regex: str,
    username: str,
    password: str,
    email: str,
    name_first: str,
    name_last: str,
    skip_slow_checks: bool = False,
) -> IAuthInfo:
    """
    Set up the server

    ### Args:
    * `address` (`str`): address for auth server

    * `request_type` (`str`): request type for auth server

    * `username_param` (`str`): username param for auth server

    * `password_param` (`str`): password param for auth server

    * `success_regex` (`str`): regex for auth success

    * `username` (`str`): username for first user

    * `password` (`str`): password for first user

    * `email` (`str`): email for first user

    * `name_first` (`str`): first name of first user

    * `name_last` (`str`): last name of first user

    * `skip_slow_checks` (`bool`, optional): whether to skip slow auth checks.
      WARNING: This is very dangerous. Defaults to `False`.

    ### Returns:
    * `User`: first registered user
    """
    if AuthConfig.exists():
        raise http_errors.Forbidden(
            "Ensemble Forum has already been set up, so this route has been "
            "disabled."
        )

    # Validate data
    assert_email_valid(email)
    assert_valid_str_field(name_first, "First name")
    assert_valid_str_field(name_last, "Last name")
    assert_valid_str_field(username, "Username")

    if not is_valid_request_type(request_type):
        raise http_errors.BadRequest(
            "Request type must be one of 'get', 'post', 'put', 'delete'"
        )

    if not skip_slow_checks:
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

        # If we give an incorrect password and it still works, then something
        # has gone terribly wrong
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
                "Authentication request succeeded in failure test. This "
                "either means that your success regular expression is "
                "matching cases where login is failing, or that your "
                "authentication system is insecure (unlikely)."
            )
    # end if not skip_slow_checks

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
                Permission.EditProfile,
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
                Permission.EditProfile,
                Permission.ReportPosts,
            ]
        },
        immutable=False,
    )

    # Initialise exam mode table and set exam mode to False
    ExamMode.initialise()

    # Create the main queue
    Queue.create(
        consts.MAIN_QUEUE,
        immutable=True,
    )
    # WARNING: Changing this order breaks the frontend. Yes, I hate this just
    # as much as you do, but it is not my fault, I am but a lowly backend
    # developer
    for name in [
        consts.REPORTED_QUEUE,
        consts.CLOSED_QUEUE,
        consts.ANSWERED_QUEUE,
        consts.DELETED_QUEUE,
    ]:
        Queue.create(
            name,
            immutable=True,
            view_only=True,
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
