from typing import cast
from ..helpers import post, get, put
from ..consts import URL
from backend.types.identifiers import UserId, PermissionId, PermissionGroupId
from backend.types.auth import JWT
from backend.types.permissions import (
    IPermissionList,
    IPermissionValues,
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


def get_permissions(token: JWT, uid: UserId) -> IPermissionValues:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:
    * `IPermissionValues`
    """
    return cast(IPermissionValues, get(
        token,
        f"{URL}/get_permissions",
        {"uid": uid}
    ))


def set_permissions(
    token: JWT,
    uid: UserId,
    permissions: dict[PermissionId, bool | None]
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
        {}
    )


def set_group(token: JWT, uid: UserId, group: PermissionGroupId) -> None:
    """
    Sets the permission group of a user.

    ## Body:
    * `uid` (`UserId`): user id to set parent permission for
    * `group` (`PermissionGroupId`): ID of permission group
    """
    put(
        token,
        f"{URL}/set_permissions",
        {
            "uid": uid,
            "group": group,
        }
    )


def groups_make(
    token: JWT,
    name: str,
    values: dict[PermissionId, bool | None],
) -> IGroupId:
    """
    Create a new permission group

    ## Body:
    * `name` (`str`): name of permission group
    * `values` (`dict[PermissionId, bool | None]`): values for permission group

    ## Returns:
    * `IGroupId`: ID for new group
    """
    return cast(IGroupId, post(
        token,
        f"{URL}/groups/make",
        {
            "name": name,
            "values": values,
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
    values: IPermissionValues,
) -> None:
    """
    Edit an existing permission group

    ## Body:
    * `group_id` (`PermissionGroupId`): permission group ID
    * `name` (`str`): new name of permission group
    * `values` (`IPermissionValues`): new values for permission group
    """
    put(
        token,
        f"{URL}/groups/make",
        {
            "group_id": group_id,
            "name": name,
            "values": values,
        }
    )
