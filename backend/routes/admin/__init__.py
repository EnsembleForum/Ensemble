"""
# Backend / Routes / Admin

Contains route definitions for functions used with administration
"""
from flask import Blueprint
from .permissions import permissions
from .users import users
from backend.models.auth_config import AuthConfig
from backend.types.auth import IAuthInfo
from backend.types.admin import IIsFirstRun


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
    * `address`: (`str`) address to query for auth
    * `username_param`: (`str`) parameter to use for username in request for
      auth
    * `password_param`: (`str`) parameter to use for password in request for
      auth
    * `success_regex`: (`str`) regular expression to check for auth success
    * `username`: (`str`) username for first user
    * `password`: (`str`) password to use with first user
    * `email`: (`str`) email for first user
    * `name_first`: (`str`) first name for first user
    * `name_last`: (`str`) last name for first user

    ## Returns:
    * `user_id`: `UserId`
    * `token`: `JWT`
    """


__all__ = [
    'admin',
]
