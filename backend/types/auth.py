"""
# Backend / Types / Auth

Types used within authentication
"""
from typing import NewType, TypedDict
from .identifiers import UserId
from .permissions import IPermissionValueGroup


JWT = NewType('JWT', str)
"""Json Web Token type"""


class IAuthInfo(TypedDict):
    """
    Authentication info, returned when logging in

    * `user_id`: `UserId`
    * `token`: `JWT`
    * `permissions`: List of objects containing:
            * `permission_id` (`int`): ID of permission
            * `value` (`bool`): whether permission is granted
    """
    user_id: UserId
    token: JWT
    permissions: list[IPermissionValueGroup]


class IUserPermissions(TypedDict):
    """
    Info on the permissions of a current user

    * `permissions`: List of objects containing:
            * `permission_id` (`int`): ID of permission
            * `value` (`bool`): whether permission is granted
    """
    permissions: list[IPermissionValueGroup]
