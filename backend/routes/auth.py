"""
# Backend / Routes / Auth

Authentication routes
"""
import json
from flask import Blueprint, request
from backend.models.user import User
from backend.models.auth_config import AuthConfig
from backend.util import http_errors
from backend.types.auth import IAuthInfo, JWT


auth = Blueprint('auth', 'auth')


@auth.post('/login')
def login() -> IAuthInfo:
    """
    Log in a user that has been registered

    ## Body:
    * `username` (`str`)
    * `password` (`str`)

    ## Returns:
    * `user_id`: `UserId`
    * `token`: `JWT`
    """
    data = json.loads(request.data.decode('utf-8'))
    username = data["username"]
    password = data["password"]
    AuthConfig().authenticate(username, password)
    try:
        u = User.from_username(username)
    except http_errors.BadRequest:
        raise http_errors.BadRequest(
            "Although the username and password are correct, this user is not "
            "registered with Ensemble. Please contact a forum administrator "
            "to get your account registered."
        ) from None
    return {
        "user_id": u.id,
        "token": JWT(f"TODO - {u.id}",)
    }


@auth.post('/logout')
def logout() -> dict:
    """
    Log out a logged in user
    """
