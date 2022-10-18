"""
# Backend / Routes / Permissions / User

Routes for managing permissions for users
"""
from flask import Blueprint
from backend.types.permissions import IPermissionUser
from backend.types.identifiers import PermissionGroupId


user = Blueprint('user', 'user')


@user.put('/set_permissions')
def set_permissions() -> dict:
    """
    Sets the permissions of a user

    ## Body:
    * `uid` (`UserId`): user id to set permissions for

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited
    """
    return {}


@user.put('/get_permissions')
def get_permissions() -> IPermissionUser:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited

    * `group_id`: the ID of the permission group this user inherits their
      permissions from
    """
    return {
        "permissions": [],
        "group_id": PermissionGroupId(-1)
    }
