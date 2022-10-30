"""
# Backend / Routes / User

Functions relating to users.
"""
import json
from flask import Blueprint, request
from backend.types.user import IUserProfile
from backend.types.identifiers import UserId
from backend.types.auth import JWT
from backend.util.tokens import uses_token
from backend.models.user import User


user = Blueprint('user', 'user')


@user.get('/profile')
@uses_token
def profile(*_) -> IUserProfile:
    """
    Returns detailed info about the

    ### Args:
    * `token` (`JWT`): token
    * `user_id` (`UserId`): user ID for user we're viewing the profile of

    ### Returns:
    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `email`: `str`
    * `user_id`: `int`

    Note that this will eventually contain more properties such as pronouns and
    the like
    """
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
    data = json.loads(request.data)
    new_name: str = data['new_name']

    user_id: UserId = data['user_id']
    user.name_last = new_name
    return User(user_id).profile()
