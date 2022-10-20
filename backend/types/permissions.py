"""
# Backend / Types / Permissions

Definitions for permission-related types used by the front-facing API
"""
from typing import TypedDict
from .identifiers import PermissionGroupId, PermissionId


class IPermissionInfo(TypedDict):
    """
    Represents a singular permission

    * permission_id

    * name
    """
    permission_id: PermissionId
    name: str


class IPermissionValueGroup(TypedDict):
    """
    Represents the value of a permission for a group. This would be far better
    as a key-value mapping, but since JSON doesn't support anything other than
    strings as keys, things kinda break a bit.

    * `permission_id`: ID of permission
    * `value` (`bool`): whether the permission is allowed or not
    """
    permission_id: PermissionId
    value: bool


class IPermissionValueUser(TypedDict):
    """
    Represents the value of a permission for a group. This would be far better
    as a key-value mapping, but since JSON doesn't support anything other than
    strings as keys, things kinda break a bit.

    * `permission_id`: ID of permission
    * `value` (`bool | None`): whether the permission is allowed (`True`),
      disallowed (`False`) or inherited (`None`)
    """
    permission_id: PermissionId
    value: bool | None


class IPermissionList(TypedDict):
    """
    List of permissions and their associated info

    * `permissions`: list containing dictionaries of

            * `permission_id`: ID of permission

            * `name`: name of permission groups
    """
    permissions: list[IPermissionInfo]


class IPermissionUser(TypedDict):
    """
    Map of permissions and their associated values

    * `permissions`: list of

            * `permission_id`: ID of permission

            * `value`: one of

                    * `True`: permission allowed

                    * `False`: permission denied

                    * `None`: permission inherited

    * `group_id`: the ID of the permission group this user inherits their
      permissions from
    """
    permissions: list[IPermissionValueUser]
    group_id: PermissionGroupId


class IPermissionGroup(TypedDict):
    """
    Info about a permission group

    * `group_id`: ID of permission group

    * `name`: name of permission group

    * `permissions`: object containing mappings, with possible values:

            * `True`: permission allowed

            * `False`: permission denied
    """
    group_id: PermissionGroupId
    name: str
    permissions: list[IPermissionValueGroup]


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
    """
    groups: list[IPermissionGroup]


class IGroupId(TypedDict):
    """
    Identifier for a group

    * `group_id`: ID of permission group
    """
    group_id: PermissionGroupId
