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


class IPermissionValues(TypedDict):
    """
    Map of permissions and their associated values

    Possible values for elements in the map are as follows:

    * `True`: permission allowed

    * `False`: permission denied

    * `None`: permission inherited
    """
    permissions: dict[PermissionId, bool | None]


class IPermissionGroup(TypedDict):
    """
    Info about a permission group
    """
    group_id: PermissionGroupId
    name: str
    permissions: IPermissionValues


class IPermissionGroupList(TypedDict):
    """
    List of info about permission groups
    """
    groups: list[IPermissionGroup]


class IGroupId(TypedDict):
    """
    Identifier for a group
    """
    group_id: PermissionGroupId
