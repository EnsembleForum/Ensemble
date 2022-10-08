"""
# Backend / Routes / Auth

Authentication routes
"""
from flask import Blueprint
from backend.types.auth import IAuthInfo


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


@auth.post('/logout')
def logout() -> dict:
    """
    Log out a logged in user
    """
