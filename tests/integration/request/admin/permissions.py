from typing import cast
from ..helpers import post, get, put, delete
from ..consts import URL
from backend.types.identifiers import UserId, PermissionId, PermissionGroupId
from backend.types.auth import JWT
from backend.types.permissions import (
    IPermissionList,
    IPermissionUser,
    IPermissionGroupList,
    IGroupId,
)

URL = f"{URL}/admin/permissions"


def list_permissions(token: JWT) -> IPermissionList:
    """
    Returns info about available permissions.

    ## Returns:
    * `IPermissionList`
    """
    return cast(IPermissionList, get(
        token,
        f"{URL}/list_permissions",
        {}
    ))


def get_permissions(token: JWT, uid: UserId) -> IPermissionUser:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:
    * `IPermissionValues`
    """
    return cast(IPermissionUser, get(
        token,
        f"{URL}/get_permissions",
        {"uid": uid}
    ))


def set_permissions(
    token: JWT,
    user_id: UserId,
    permissions: dict[PermissionId, bool | None],
    group_id: PermissionGroupId,
) -> None:
    """
    Sets the permissions of a user

    ## Body:
    * `uid` (`UserId`): user id to set permissions for
    * `permissions`: (`dict[PermissionId, bool?]`): mapping of permission IDs
    """
    put(
        token,
        f"{URL}/set_permissions",
        {
            "user_id": user_id,
            "permissions": permissions,
            "group_id": group_id,
        }
    )


def groups_create(
    token: JWT,
    name: str,
    permissions: dict[PermissionId, bool],
) -> IGroupId:
    """
    Create a new permission group

    ## Body:
    * `name` (`str`): name of permission group
    * `permissions` (`dict[PermissionId, bool | None]`): values for permission
      group

    ## Returns:
    * `IGroupId`: ID for new group
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
    List available permission groups

    ## Returns:
    * `IPermissionGroupList`
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
    permissions: dict[PermissionId, bool],
) -> None:
    """
    Edit an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    * `name` (`str`): new name of permission group
    * `permissions` (`IPermissionValues`): new values for permission group
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

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    """
    delete(
        token,
        f"{URL}/groups/remove",
        {
            "group_id": group_id,
            "transfer_group_id": transfer_group_id,
        }
    )
