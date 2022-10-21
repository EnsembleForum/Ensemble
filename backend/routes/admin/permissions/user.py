"""
# Backend / Routes / Permissions / User

Routes for managing permissions for users
"""
import json
from flask import Blueprint, request
from backend.types.permissions import IPermissionUser
from backend.types.identifiers import PermissionGroupId, UserId
from backend.models.user import User
from backend.util.tokens import uses_token
from backend.util.http_errors import BadRequest
from backend.types.permissions import (
    IPermissionValueUser,
)
from backend.models.permissions import (
    PermissionGroup,
    Permission,
    map_permissions_user,
)


user = Blueprint('user', 'user')


@user.put('/set_permissions')
@uses_token
def set_permissions(user: User, *_) -> dict:
    """
    Sets the permissions of a user

    ## Body:
    * `user_id` (`UserId`): user id to set permissions for

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited

    * `group_id`: the ID of the permission group this user inherits their
      permissions from
    """
    user.permissions.assert_can(Permission.ManageUserPermissions)
    data = json.loads(request.data)
    target_user = User(UserId(data['user_id']))
    permissions: list[IPermissionValueUser] = data['permissions']
    group = PermissionGroup(PermissionGroupId(data['group_id']))

    if target_user == user:
        raise BadRequest("Users cannot set their own permissions")

    target_user.permissions.update_allowed(map_permissions_user(permissions))
    target_user.permissions.parent = group

    return {}


@user.get('/get_permissions')
@uses_token
def get_permissions(user: User, *_) -> IPermissionUser:
    """
    Returns the permissions of a user

    ## Params:
    * `user_id` (`UserId`): user id to query permissions for

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
    user.permissions.assert_can(Permission.ManageUserPermissions)
    target_user = User(UserId(int(request.args['user_id'])))
    permissions = target_user.permissions

    return {
        "permissions": [
            {
                "permission_id": p.value,
                "value": permissions.value(p),
            }
            for p in Permission
        ],
        "group_id": permissions.parent.id
    }