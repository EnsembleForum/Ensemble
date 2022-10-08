"""
# Backend / Types / Identifiers

Identifier types used for additional type safety.

These are used to prevent interchangeability between different types of
identifiers.
"""
from typing import NewType

UserId = NewType('UserId', int)
PermissionId = NewType('PermissionId', int)
UserPermissionId = NewType('UserPermissionId', int)
PermissionGroupId = NewType('PermissionGroupId', int)
