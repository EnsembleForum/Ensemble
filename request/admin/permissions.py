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

    ## Header
    * `token` (`str`): JWT of the user

    ## Returns
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

    ## Header
    * `token` (`str`): JWT of the user

    ## Params
    * `user_id` (`int`): user id to query permissions for

    ## Returns:

    * `permissions`: list of

            * `permission_id` (`int`): ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited

    * `group_id` (`int`): the ID of the permission group this user inherits
      their permissions from
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

    ## Header
    * `token` (`str`): JWT of the user

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
    * `token` (`str`): JWT of the user

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
    ### POST `/admin/permissions/groups/list`

    List available permission groups

    ## Header
    * `token` (`str`): JWT of the user

    ## Returns

    * `groups`: list of info about permission groups. Each entry is an object
      containing:

            * `group_id` (`int`): ID of permission group

            * `name` (`str`): name of permission group

            * `permissions`: object containing mappings, with possible values:

                    * `True`: permission allowed

                    * `False`: permission denied
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
    * `token` (`str`): JWT of the user

    ## Body
    * `group_id` (`int`): permission group ID

    * `name` (`str`): new name of permission group

    * `permissions`: list of

            * `permission_id` (`int`): ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied
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
    Remove an existing permission group

    ## Header
    * `token` (`str`): JWT of the user

    ## Params
    * `group_id` (`int`): permission group ID
    """
    delete(
        token,
        f"{URL}/groups/remove",
        {
            "group_id": group_id,
            "transfer_group_id": transfer_group_id,
        }
    )
