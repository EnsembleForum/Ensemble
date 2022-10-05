from flask import Blueprint
from backend.models.permissions import PermissionGroup
from backend.types.permissions import (
    IPermissionList,
    IPermissionValues,
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
    * `IPermissionList`
    """


@permissions.get('/get_permissions')
def get_permissions() -> IPermissionValues:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:
    * `IPermissionValues`
    """


@permissions.put('/set_permissions')
def set_permissions() -> dict:
    """
    Sets the permissions of a user

    ## Body:
    * `uid` (`UserId`): user id to set permissions for
    * `permissions`: (`dict[PermissionId, bool?]`): mapping of permission IDs
    """


@permissions.put('/set_group')
def set_group() -> dict:
    """
    Sets the permission group of a user.

    ## Body:
    * `uid` (`UserId`): user id to set parent permission for
    * `group` (`PermissionGroupId`): ID of permission group
    """


@permissions.post('/groups/make')
def groups_make() -> IGroupId:
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
    * `IPermissionGroupList`
    """


@permissions.put('/groups/edit')
def groups_edit() -> dict:
    """
    Edit an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    * `name` (`str`): new name of permission group
    * `values` (`IPermissionValues`): new values for permission group
    """
