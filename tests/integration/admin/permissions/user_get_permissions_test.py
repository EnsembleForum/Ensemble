"""
# Tests / Integration / Admin / Permissions / User get permissions test

Tests for getting the specific permissions of users.

* Error if we don't have permission
* User ID not valid
* Admins can view permissions of other users
"""
import pytest
from ensemble_request.admin.permissions import get_permissions
from tests.integration.conftest import ISimpleUsers, IPermissionGroups
from backend.util.http_errors import Forbidden
from backend.types.identifiers import UserId


def test_no_permission(
    simple_users: ISimpleUsers,
):
    """Do we get an error if we don't have permission to view user permissions?
    """
    with pytest.raises(Forbidden):
        get_permissions(
            simple_users['mod']['token'],
            simple_users['admin']['user_id'],
        )


def test_invalid_user_id(
    simple_users: ISimpleUsers,
):
    """Do we get an error if we give an invalid user ID?"""
    with pytest.raises(Forbidden):
        get_permissions(
            simple_users['mod']['token'],
            UserId(-1),
        )


def test_view_permissions(
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """Can we view other users permissions if we're an admin?"""
    perms = get_permissions(
            simple_users['admin']['token'],
            simple_users['mod']['user_id'],
        )
    # Make sure they're a moderator
    assert perms['group_id'] == permission_groups['mod']['group_id']
    # Make sure they don't have any other permissions
    for v in perms['permissions']:
        assert v['value'] is None
