"""
# Backend / Routes / Auth

Authentication routes
"""
import json
from flask import Blueprint, request
from backend.models.user import User
from backend.models.auth_config import AuthConfig
from backend.models.token import Token
from backend.models.permissions import Permission
from backend.util import http_errors
from backend.types.auth import IAuthInfo, JWT


auth = Blueprint('auth', 'auth')


@auth.post('/login')
def login() -> IAuthInfo:
    # Check if they have a token
    if (tok := request.headers.get('Authorization', None)) is not None:
        try:
            Token.fromJWT(JWT(tok.removeprefix('Bearer ')))
        except http_errors.Forbidden:
            pass
        else:
            raise http_errors.BadRequest(
                "You're already logged in - return to the main page to see "
                "the content"
            )
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
        "token": Token.create(u).encode(),
        "permissions": [
            {
                "permission_id": p.value,
                "value": u.permissions.can(p),
            } for p in Permission
        ],
    }


@auth.post('/logout')
def logout() -> dict:
    # TODO: Fix up this so that it's more robust
    token = JWT(request.headers['Authorization'].removeprefix('Bearer '))
    try:
        Token.fromJWT(token).invalidate()
    except http_errors.Forbidden:
        # If we get an error do nothing, to prevent a painful experience if a
        # user doesn't have a valid token and wants to return to the login
        # screen
        pass
    return {}
