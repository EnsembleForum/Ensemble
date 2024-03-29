from typing import cast
from ..helpers import post, get, put, delete
from ..consts import URL
from backend.types.identifiers import UserId, PermissionGroupId
from backend.types.auth import JWT
from backend.types.permissions import (
    IPermissionList,
    IPermissionUser,
    IPermissionGroupList,
    IGroupId,
    IPermissionValueGroup,
    IPermissionValueUser,
)

URL = f"{URL}/admin/permissions"


def list_permissions(token: JWT) -> IPermissionList:
    """
    ### GET `/admin/permissions/list_permissions`

    Returns info about available permissions.

    This route is deprecated, as permissions are now stored in
    `resources/permissions.json`, which can be accessed by the frontend.

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Returns
    Object containing:
    * `permissions`: list containing dictionaries of

            * `permission_id` (`int`): ID of permission

            * `name` (`str`): name of permission groups
    """
    return cast(IPermissionList, get(
        token,
        f"{URL}/list_permissions",
        {}
    ))


def get_permissions(token: JWT, user_id: UserId) -> IPermissionUser:
    """
    ### GET `/admin/permissions/user/get_permissions`

    Returns the permissions of a user

    ## Permissions
    * `ManageUserPermissions`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `user_id` (`int`): user id to query permissions for

    ## Returns
    Object containing:
    * `permissions`: list of
            * `permission_id` (`int`): ID of permission
            * `value`: one of
                    * `True`: permission allowed
                    * `False`: permission denied
                    * `None`: permission inherited
    * `group_id` (`int`): the ID of the permission group this user inherits
      their permissions from

    ## Errors

    ### 403
    * User does not have permission `ManageUserPermissions`
    """
    return cast(IPermissionUser, get(
        token,
        f"{URL}/user/get_permissions",
        {"user_id": user_id}
    ))


def set_permissions(
    token: JWT,
    user_id: UserId,
    permissions: list[IPermissionValueUser],
    group_id: PermissionGroupId,
) -> None:
    """
    ### PUT `/admin/permissions/user/set_permissions`

    Sets the permissions of a user

    ## Permissions
    * `ManageUserPermissions`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `user_id` (`int`): user id to set permissions for
    * `permissions`: list of
            * `permission_id` (`int`): ID of permission
            * `value`: one of
                    * `True`: permission allowed
                    * `False`: permission denied
                    * `None`: permission inherited
    * `group_id`: the ID of the permission group this user inherits their
      permissions from

    ## Errors

    ### 400
    * User attempting to set their own permissions
    * Not all permission values specified

    ### 403
    * User does not have permission `ManageUserPermissions`
    """
    put(
        token,
        f"{URL}/user/set_permissions",
        {
            "user_id": user_id,
            "permissions": permissions,
            "group_id": group_id,
        }
    )


def groups_create(
    token: JWT,
    name: str,
    permissions: list[IPermissionValueGroup],
) -> IGroupId:
    """
    ### POST `/admin/permissions/groups/create`

    Create a new permission group

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `name` (`str`): name of permission group
    * `permissions`: list of
            * `permission_id` (`int`): ID of permission
            * `value`: one of
                    * `True`: permission allowed
                    * `False`: permission denied

    ## Returns
    Object containing:
    * `group_id` (`int`): ID for new group

    ## Errors

    ### 400
    * A permission group with the given name already exists
    * Not all permission values specified
    * Name of permission group is empty

    ### 403
    * User does not have permission `ManagePermissionGroups`
    """
    return cast(IGroupId, post(
        token,
        f"{URL}/groups/create",
        {
            "name": name,
            "permissions": permissions,
        }
    ))


def groups_list(token: JWT) -> IPermissionGroupList:
    """
    ### GET `/admin/permissions/groups/list`

    List available permission groups

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Returns
    Object containing:
    * `groups`: list of info about permission groups. Each entry is an object
      containing:
            * `group_id` (`int`): ID of permission group
            * `name` (`str`): name of permission group
            * `permissions`: object containing mappings, with possible values:
                    * `True`: permission allowed
                    * `False`: permission denied

    ## Errors

    ### 403
    * User does not have permission `ManagePermissionGroups`
    """
    return cast(IPermissionGroupList, get(
        token,
        f"{URL}/groups/list",
        {}
    ))


def groups_edit(
    token: JWT,
    group_id: PermissionGroupId,
    name: str,
    permissions: list[IPermissionValueGroup],
) -> None:
    """
    ### PUT `/admin/permissions/groups/edit`

    Edit an existing permission group

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `group_id` (`int`): permission group ID
    * `name` (`str`): new name of permission group
    * `permissions`: list of
            * `permission_id` (`int`): ID of permission
            * `value`: one of
                    * `True`: permission allowed
                    * `False`: permission denied

    ## Errors

    ### 400
    * Permission group with given ID not found
    * A permission group with the given new name already exists and isn't this
      group
    * Not all permission values specified
    * New name of permission group is empty
    * Cannot edit immutable permission groups (ie Administrator)

    ### 403
    * User does not have permission `ManagePermissionGroups`
    """
    put(
        token,
        f"{URL}/groups/edit",
        {
            "group_id": group_id,
            "name": name,
            "permissions": permissions,
        }
    )


def groups_remove(
    token: JWT,
    group_id: PermissionGroupId,
    transfer_group_id: PermissionGroupId,
) -> None:
    """
    ### DELETE `/admin/permissions/groups/remove`

    Remove an existing permission group

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `group_id` (`int`): permission group ID

    ## Errors

    ### 400
    * Permission group with given ID not found
    * Cannot transfer users to the same permission group
    * Cannot remove immutable permission groups

    ### 403
    * User does not have permission `ManagePermissionGroups`
    """
    delete(
        token,
        f"{URL}/groups/remove",
        {
            "group_id": group_id,
            "transfer_group_id": transfer_group_id,
        }
    )
