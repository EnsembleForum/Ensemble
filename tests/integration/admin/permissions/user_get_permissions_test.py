"""
# Tests / Integration / Admin / Permissions / User get permissions test

Tests for getting the specific permissions of users.

* Error if we don't have permission
* User ID not valid
* Admins can view permissions of other users
"""
import pytest
from tests.integration.request.admin.permissions import get_permissions
from tests.integration.conftest import IAllUsers, IPermissionGroups
from backend.util.http_errors import Forbidden
from backend.types.identifiers import UserId


def test_no_permission(
    all_users: IAllUsers,
):
    """Do we get an error if we don't have permission to view user permissions?
    """
    with pytest.raises(Forbidden):
        get_permissions(
            all_users['mods'][0]['token'],
            all_users['admins'][0]['user_id'],
        )


def test_invalid_user_id(
    all_users: IAllUsers,
):
    """Do we get an error if we give an invalid user ID?"""
    with pytest.raises(Forbidden):
        get_permissions(
            all_users['mods'][0]['token'],
            UserId(-1),
        )


def test_view_permissions(
    all_users: IAllUsers,
    permission_groups: IPermissionGroups,
):
    """Can we view other users permissions if we're an admin?"""
    perms = get_permissions(
            all_users['admins'][0]['token'],
            all_users['mods'][0]['user_id'],
        )
    # Make sure they're a moderator
    assert perms['group_id'] == permission_groups['mod']['group_id']
    # Make sure they don't have any other permissions
    for v in perms['permissions']:
        assert v['value'] is None
