"""
# Backend / Types / Permissions

Definitions for permission-related types used by the front-facing API
"""
from typing import TypedDict
from .identifiers import PermissionGroupId, PermissionId


class IPermissionInfo(TypedDict):
    """
    Represents a singular permission
    """
    perm_id: PermissionId
    name: str


class IPermissionList(TypedDict):
    """
    List of permissions and their associated info
    """
    permissions: list[IPermissionInfo]


class IPermissionUser(TypedDict):
    """
    Map of permissions and their associated values

    * `permissions`: object containing mappings, with possible values:

            * `True`: permission allowed

            * `False`: permission denied

            * `None`: permission inherited

    * `group_id`: the ID of the permission group this user inherits their
      permissions from
    """
    permissions: dict[PermissionId, bool | None]
    group_id: PermissionGroupId


class IPermissionGroup(TypedDict):
    """
    Info about a permission group

    * `group_id`: ID of permission group

    * `name`: name of permission group

    * `permissions`: object containing mappings, with possible values:

            * `True`: permission allowed

            * `False`: permission denied

            * `None`: permission inherited
    """
    group_id: PermissionGroupId
    name: str
    permissions: dict[PermissionId, bool | None]


class IPermissionGroupList(TypedDict):
    """
    List of info about permission groups

    * `groups`: list of info about permission groups. Each entry is an object
      containing:

            * `group_id`: ID of permission group

            * `name`: name of permission group

            * `permissions`: object containing mappings, with possible values:

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited
    """
    groups: list[IPermissionGroup]


class IGroupId(TypedDict):
    """
    Identifier for a group

    * `group_id`: ID of permission group
    """
    group_id: PermissionGroupId
