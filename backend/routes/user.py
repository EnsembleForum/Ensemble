"""
# Backend / Routes / User

Functions relating to users.
"""
from flask import Blueprint, request
from backend.types.user import IUserProfile
from backend.types.identifiers import UserId
from backend.util.tokens import uses_token
from backend.models.user import User


user = Blueprint('user', 'user')


@user.get('/profile')
@uses_token
def profile(*_) -> IUserProfile:
    user_id = UserId(request.args["user_id"])
    return User(user_id).profile()
