from typing import cast
from ..helpers import post, get, put
from ..consts import URL
from backend.types.identifiers import UserId, PermissionId, PermissionGroupId
from backend.types.permissions import (
    IPermissionList,
    IPermissionValues,
    IPermissionGroupList,
)

URL = f"{URL}/admin/permissions"


def list_permissions() -> IPermissionList:
    """
    Returns info about available permissions.

    ## Returns:
    * `IPermissionList`
    """
    return cast(IPermissionList, get(
        f"{URL}/list_permissions",
        {}
    ))


def get_permissions(uid: UserId) -> IPermissionValues:
    """
    Returns the permissions of a user

    ## Params:
    * `uid` (`UserId`): user id to query permissions for

    ## Returns:
    * `IPermissionValues`
    """
    return cast(IPermissionValues, get(
        f"{URL}/get_permissions",
        {"uid": uid}
    ))


def set_permissions(
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
        f"{URL}/set_permissions",
        {}
    )


def set_group(uid: UserId, group: PermissionGroupId) -> None:
    """
    Sets the permission group of a user.

    ## Body:
    * `uid` (`UserId`): user id to set parent permission for
    * `group` (`PermissionGroupId`): ID of permission group
    """
    put(
        f"{URL}/set_permissions",
        {
            "uid": uid,
            "group": group,
        }
    )


def groups_make(name: str, values: IPermissionValues) -> None:
    """
    Create a new permission group

    ## Body:
    * `name` (`str`): name of permission group
    * `values` (`IPermissionValues`): values for permission group
    """
    post(
        f"{URL}/groups/make",
        {
            "name": name,
            "values": values,
        }
    )


def groups_list() -> IPermissionGroupList:
    """
    List available permission groups

    ## Returns:
    * `IPermissionGroupList`
    """
    return cast(IPermissionGroupList, get(
        f"{URL}/groups/list",
        {}
    ))


def groups_edit(
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
        f"{URL}/groups/make",
        {
            "group_id": group_id,
            "name": name,
            "values": values,
        }
    )
