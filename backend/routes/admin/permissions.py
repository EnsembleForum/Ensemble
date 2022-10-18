from flask import Blueprint
from backend.models.permissions import PermissionGroup, Permission
from backend.types.permissions import (
    IPermissionList,
    IPermissionUser,
    IPermissionGroupList,
    IGroupId,
)
from backend.types.identifiers import PermissionGroupId


permissions = Blueprint('permissions', 'permissions')


@permissions.get('/list_permissions')
def list_permissions() -> IPermissionList:
    """
    Returns info about available permissions.

    ## Returns:

    * permissions: list containing dictionaries of

            * permission_id

            * name
    """
    return {
        "permissions": [
            {
                "permission_id": p.value,
                "name": p.name,
            }
            for p in Permission
        ]
    }


@permissions.get('/get_permissions')
def get_permissions() -> IPermissionUser:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:

    * `permissions`: object containing mappings, with possible values:

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


@permissions.put('/set_permissions')
def set_permissions() -> dict:
    """
    Sets the permissions of a user

    ## Body:
    * `uid` (`UserId`): user id to set permissions for
    * `permissions`: (`dict[PermissionId, bool?]`): mapping of permission IDs
    """
    return {}


@permissions.put('/set_group')
def set_group() -> dict:
    """
    Sets the permission group of a user.

    ## Body:
    * `uid` (`UserId`): user id to set parent permission for
    * `group` (`PermissionGroupId`): ID of permission group
    """
    return {}


@permissions.post('/groups/create')
def groups_create() -> IGroupId:
    """
    Create a new permission group

    ## Body:
    * `name` (`str`): name of permission group
    * `values` (`dict[PermissionId, bool | None]`): values for permission group

    ## Returns:
    * `IGroupId`: ID for new group
    """
    PermissionGroup.create('Test', {})
    return {
        "group_id": PermissionGroupId(1)
    }


@permissions.get('/groups/list')
def groups_list() -> IPermissionGroupList:
    """
    List available permission groups

    ## Returns:

    * `groups`: list of info about permission groups. Each entry is an object
      containing:

            * `group_id`: ID of permission group

            * `name`: name of permission group

            * `permissions`: object containing mappings, with possible values:

                    * `True`: permission allowed

                    * `False`: permission denied
    """
    groups = PermissionGroup.all()
    return {"groups": [
        {
            "group_id": g.id,
            "name": g.name,
            "permissions": [
                {
                    "permission_id": p.value,
                    "value": g.can(p),
                }
                for p in Permission
            ]
        }
        for g in groups
    ]}


@permissions.put('/groups/edit')
def groups_edit() -> dict:
    """
    Edit an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    * `name` (`str`): new name of permission group
    * `values` (`IPermissionValues`): new values for permission group
    """
    return {}
