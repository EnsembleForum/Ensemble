"""
# Backend / Models

Contains code for the data structures used internally by the backend.
"""
from .permissions.permission import Permission
from .permissions.permission_set import PermissionSet

__all__ = [
    'Permission',
    'PermissionSet',
]

# Initialise the database
from . import piccolo_app
from . import tables
del piccolo_app
del tables
