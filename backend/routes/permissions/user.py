"""
# Backend / Routes / Permissions / User

Routes for managing permissions for users
"""
from flask import Blueprint
from backend.types.permissions import IPermissionUser
from backend.types.identifiers import PermissionGroupId


user = Blueprint('user', 'permissions.user')


@user.put('/set_permissions')
def set_permissions() -> dict:
    return {}


@user.put('/get_permissions')
def get_permissions() -> IPermissionUser:
    return {
        "permissions": {},
        "group_id": PermissionGroupId(1),
    }
