from flask import Blueprint
from backend.types.permissions import (
    IPermissionList,
    IPermissionValues,
    IPermissionGroupList,
)


permissions = Blueprint('permissions', 'permissions')


@permissions.get('/list')
def list_permissions() -> IPermissionList:
    """
    Returns info about available permissions.

    ## Returns:
    * `IPermissionList`
    """


@permissions.get('/get')
def query_permission() -> IPermissionValues:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:
    * `IPermissionValues`
    """


@permissions.put('/set')
def set_permission() -> dict:
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
    * `parent` (`PermissionGroupId`): ID of permission group
    """


@permissions.post('/groups/make')
def group_make() -> dict:
    """
    Create a new permission group

    ## Body:
    * `name` (`str`): name of permission group
    * `values` (`IPermissionValues`): values for permission group
    """


@permissions.get('/groups/list')
def group_list() -> IPermissionGroupList:
    """
    List available permission groups
    """


@permissions.put('/groups/edit')
def group_edit() -> dict:
    """
    Edit an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    * `name` (`str`): new name of permission group
    * `values` (`IPermissionValues`): new values for permission group
    """
