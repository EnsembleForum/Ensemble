"""
# Backend / Routes / Permissions / User

Routes for managing permissions for users
"""
from flask import Blueprint


user = Blueprint('user', 'permissions.user')


@user.put('/set_permissions')
def set_permissions():
    return {}


@user.put('/get_permissions')
def get_permissions():
    return {}
