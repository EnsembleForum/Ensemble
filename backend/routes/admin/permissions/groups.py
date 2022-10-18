"""
# Backend / Routes / Permissions / Groups

Routes for managing permission groups
"""
import json
from flask import Blueprint, request
from backend.types.identifiers import PermissionGroupId
from backend.types.permissions import (
    IGroupId,
    IPermissionGroupList,
    IPermissionValueGroup,
)
from backend.models.permissions import (
    PermissionGroup,
    Permission,
    map_permissions_group,
)


groups = Blueprint('groups', 'groups')


@groups.post('/create')
def create() -> IGroupId:
    """
    Create a new permission group

    ## Body:
    * `name` (`str`): name of permission group

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited

    ## Returns:
    * `IGroupId`: ID for new group
    """
    data = json.loads(request.data)
    name = data['name']
    permissions: list[IPermissionValueGroup] = data['permissions']
    print(permissions)
    mapped_perms = map_permissions_group(permissions)
    group = PermissionGroup.create(name, mapped_perms)
    return {
        "group_id": group.id
    }


@groups.get('/list')
def list_groups() -> IPermissionGroupList:
    """
    List available permission groups

    ## Returns:

    * `groups`: list of info about permission groups. Each entry is an object
      containing:

            * `group_id`: ID of permission group

            * `name`: name of permission group

            * `permissions`: list of

                    * `permission_id`: ID of permission

                    * `value`: one of

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


@groups.put('/edit')
def edit() -> dict:
    """
    Edit an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID

    * `name` (`str`): new name of permission group

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited
    """
    data = json.loads(request.data)
    group = PermissionGroup(PermissionGroupId(data['group_id']))
    name = data['name']
    permissions: list[IPermissionValueGroup] = data['permissions']

    group.name = name
    group.update_allowed(map_permissions_group(permissions))
    return {}


@groups.delete('/remove')
def remove() -> dict:
    """
    Remove an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    """
    data = json.loads(request.data)
    group = PermissionGroup(PermissionGroupId(data['group_id']))
    group.delete()
    return {}
