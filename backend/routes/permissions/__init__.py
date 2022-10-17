"""
# Backend / Routes / Permissions

Routes for managing permissions
"""
from flask import Blueprint
from .groups import groups
from .user import user
from backend.types.permissions import IPermissionList


permissions = Blueprint('permissions', 'permissions')


permissions.register_blueprint(groups, url_prefix="/groups")
permissions.register_blueprint(user, url_prefix="/user")


@permissions.get('/list_permissions')
def list_permissions() -> IPermissionList:
    return {
        "permissions": []
    }
