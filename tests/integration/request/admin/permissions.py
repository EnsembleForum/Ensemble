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
    IPermissionValueGroup,
    IPermissionValueUser,
)

URL = f"{URL}/admin/permissions"


def list_permissions(token: JWT) -> IPermissionList:
    """
    Returns info about available permissions.

    ## Returns:
    * `permissions`: list containing dictionaries of

            * `permission_id`: ID of permission

            * `name` (`str`): name of permission groups
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

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited

    * `group_id`: the ID of the permission group this user inherits their
      permissions from
    """
    return cast(IPermissionUser, get(
        token,
        f"{URL}/user/get_permissions",
        {"uid": uid}
    ))


def set_permissions(
    token: JWT,
    user_id: UserId,
    permissions: list[IPermissionValueUser],
    group_id: PermissionGroupId,
) -> None:
    """
    Sets the permissions of a user

    ## Body:
    * `uid` (`UserId`): user id to set permissions for

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited
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
    permissions: dict[PermissionId, bool],
) -> IGroupId:
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

    * `groups`: list of info about permission groups. Each entry is an object
      containing:

            * `group_id`: ID of permission group

            * `name`: name of permission group

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
