"""
# Backend / Routes / User

Functions relating to users.
"""
import json
from typing import Optional
from flask import Blueprint, request
from backend.models import Permission, User
from backend.types.user import IUserProfile
from backend.types.identifiers import UserId
from backend.util.tokens import uses_token


user = Blueprint('user', 'user')


@user.get('/profile')
@uses_token
def profile(*_) -> IUserProfile:
    user_id = UserId(request.args["user_id"])
    return User(user_id).profile()


@user.put('/profile/edit_name_first')
@uses_token
def edit_name_first(user: User, *_) -> dict:
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
    data = json.loads(request.data)
    subject = User(UserId(data['user_id']))
    name_first: str = data['name_first']

    if user == subject:
        user.permissions.assert_can(Permission.EditProfile)
    else:
        user.permissions.assert_can(Permission.ManageUserProfiles)

    subject.name_first = name_first
    return {}


@user.put('/profile/edit_name_last')
@uses_token
def edit_name_last(user: User, *_) -> dict:
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
    data = json.loads(request.data)
    name_last: str = data['name_last']
    subject = User(UserId(data['user_id']))

    if user == subject:
        user.permissions.assert_can(Permission.EditProfile)
    else:
        user.permissions.assert_can(Permission.ManageUserProfiles)

    subject.name_last = name_last
    return {}


@user.put('/profile/edit_email')
@uses_token
def edit_email(user: User, *_) -> dict:
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
    data = json.loads(request.data)
    email: str = data['email']
    subject = User(UserId(data['user_id']))

    if user == subject:
        user.permissions.assert_can(Permission.EditProfile)
    else:
        user.permissions.assert_can(Permission.ManageUserProfiles)

    subject.email = email
    return {}


@user.put('/profile/edit_pronouns')
@uses_token
def edit_pronouns(user: User, *_) -> dict:
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
    data = json.loads(request.data)
    pronouns: Optional[str] = data['pronouns']
    subject = User(UserId(data['user_id']))

    if user == subject:
        user.permissions.assert_can(Permission.EditProfile)
    else:
        user.permissions.assert_can(Permission.ManageUserProfiles)

    subject.pronouns = pronouns
    return {}
