"""
# Backend / Routes / Permissions / Groups

Routes for managing permission groups
"""
from flask import Blueprint
from backend.types.identifiers import PermissionGroupId
from backend.types.permissions import IGroupId, IPermissionGroupList
from backend.models.permissions import PermissionGroup, Permission


groups = Blueprint('groups', 'admin.permissions.groups')


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
    PermissionGroup.create('Test', {})
    return {
        "group_id": PermissionGroupId(1)
    }


@groups.get('/list')
def list() -> IPermissionGroupList:
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
    return {}


@groups.delete('/remove')
def remove() -> dict:
    """
    Remove an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    """
    return {}
