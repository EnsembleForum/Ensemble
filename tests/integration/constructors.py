"""
# Tests / Integration / Constructors

Code for building common code objects used by tests
"""
from .functions.admin.permissions import groups_make
from backend.types.identifiers import PermissionGroupId


def basic_permission_group() -> PermissionGroupId:
    """
    Create a basic permission group

    This should be done automatically on server initialisation at some point,
    but for now I'm putting this here to make life easier.
    """
    return groups_make(
        "User",
        {},
    )["group_id"]
