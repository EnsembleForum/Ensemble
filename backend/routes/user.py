"""
# Backend / Routes / User

Functions relating to users.
"""
import json
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.types.user import IUserProfile
from backend.types.identifiers import UserId
from backend.util.tokens import uses_token
from backend.models.user import User
from backend.util import http_errors


user = Blueprint('user', 'user')


@user.get('/profile')
@uses_token
def profile(*_) -> IUserProfile:
    user_id = UserId(request.args["user_id"])
    return User(user_id).profile()


@user.put('/profile/edit_name_first')
@uses_token
def edit_name_first(user: User, *_) -> IUserProfile:
    """
    Edits username's profile

    ### Args:
    * `token` (`JWT`): token
    * `user_id` (`UserId`): user ID for user we're viewing the profile of

    ### Returns:
    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `email`: `str`
    * `user_id`: `int`

    """
    user.permissions.assert_can(Permission.EditName)
    if not user.can_edit_name():
        raise http_errors.Forbidden(
            "Do not have permissions to edit others names"
            )
    data = json.loads(request.data)
    new_name: str = data['new_name']
    user_id: UserId = data['user_id']
    user.name_first = new_name
    return User(user_id).profile()


@user.put('/profile/edit_name_last')
@uses_token
def edit_name_last(user: User, *_) -> IUserProfile:
    """
    Edits username's profile

    ### Args:
    * `token` (`JWT`): token
    * `user_id` (`UserId`): user ID for user we're viewing the profile of

    ### Returns:
    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `email`: `str`
    * `user_id`: `int`

    """
    user.permissions.assert_can(Permission.EditName)
    if not user.can_edit_name():
        raise http_errors.Forbidden(
            "Do not have permissions to edit others names"
            )
    data = json.loads(request.data)
    new_name: str = data['new_name']

    user_id: UserId = data['user_id']
    user.name_last = new_name
    return User(user_id).profile()
