"""
# Tests / Integration / Admin / Permissions / Groups delete

Tests for deleting permission groups

* Group ID doesn't exist
* Transfer group ID doesn't exist
* Can't delete the admin group
* Don't have ManageGroupPermissions permission
* Group removed
* Group members transferred
"""
import pytest
from tests.integration.conftest import (
    IBasicServerSetup,
    ISimpleUsers,
    IPermissionGroups,
)
from ensemble_request.admin import permissions
from backend.util.http_errors import Forbidden, BadRequest
from backend.types.identifiers import PermissionGroupId


def test_group_id_invalid(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we give an invalid group ID?
    """
    with pytest.raises(BadRequest):
        permissions.groups_remove(
            basic_server_setup['token'],
            PermissionGroupId(-1),
            permission_groups['user']['group_id'],
        )


def test_transfer_group_id_invalid(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we give an invalid transfer group ID?
    """
    with pytest.raises(BadRequest):
        permissions.groups_remove(
            basic_server_setup['token'],
            permission_groups['user']['group_id'],
            PermissionGroupId(-1),
        )


def test_admin_group_immutable(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we try to remove the administrator group?
    """
    # Try to make admins turn to mods
    with pytest.raises(BadRequest):
        permissions.groups_remove(
            basic_server_setup['token'],
            permission_groups['admin']['group_id'],
            permission_groups['mod']['group_id'],
        )


def test_group_transfer_to_same(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we try to transfer users to the same group?
    """
    # Try to make nods turn into mods
    with pytest.raises(BadRequest):
        permissions.groups_remove(
            basic_server_setup['token'],
            permission_groups['mod']['group_id'],
            permission_groups['mod']['group_id'],
        )


def test_no_permission(
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """Do we get an error if we don't have permission?"""
    with pytest.raises(Forbidden):
        permissions.groups_remove(
            simple_users['mod']['token'],
            permission_groups['mod']['group_id'],
            permission_groups['admin']['group_id'],
        )


def test_permissions_removed(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """Does the group get removed?"""
    permissions.groups_remove(
        basic_server_setup['token'],
        permission_groups['mod']['group_id'],
        permission_groups['user']['group_id'],
    )
    new_groups = permissions.groups_list(basic_server_setup['token'])['groups']
    # Make sure it got removed
    assert len(new_groups) == 2


def test_users_transferred(
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """Do the users get transferred?"""
    permissions.groups_remove(
        simple_users['admin']['token'],
        permission_groups['mod']['group_id'],
        permission_groups['user']['group_id'],
    )
    # Make sure the moderators got moved into the users group
    assert permissions.get_permissions(
        simple_users['admin']['token'],
        simple_users['mod']['user_id'],
    )['group_id'] == permission_groups['user']['group_id']
