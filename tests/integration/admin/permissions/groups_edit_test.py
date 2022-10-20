"""
# Tests / Integration / Admin / Permissions / Groups edit

Tests for editing permission groups

* Group name already taken
* Group ID doesn't exist
* Can't edit the admin group
* Don't have ManageGroupPermissions permission
* Users in edited groups get permissions
* Name updates
"""
import pytest
from tests.integration.conftest import (
    IBasicServerSetup,
    IAllUsers,
    IPermissionGroups,
)
from request.admin import permissions
from backend.models.permissions.permission import Permission
from backend.util.http_errors import Forbidden, BadRequest
from backend.types.identifiers import PermissionGroupId


def test_group_name_taken(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we rename a group to a name that's already taken?
    """
    # Rename mods to be the same as users
    with pytest.raises(BadRequest):
        permissions.groups_edit(
            basic_server_setup['token'],
            permission_groups['mod']['group_id'],
            permission_groups['user']['name'],
            permission_groups['mod']['permissions'],
        )


def test_bad_id(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we give an invalid group ID?
    """
    # Rename group 1 to be the same as group 2
    with pytest.raises(BadRequest):
        permissions.groups_edit(
            basic_server_setup['token'],
            PermissionGroupId(-1),
            permission_groups['mod']['name'],
            permission_groups['mod']['permissions'],
        )


def test_admin_group_immutable(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we try to edit the administrator group?
    """
    # Rename group 1 to be the same as group 2
    with pytest.raises(BadRequest):
        permissions.groups_edit(
            basic_server_setup['token'],
            permission_groups['admin']['group_id'],
            permission_groups['admin']['name'],
            permission_groups['mod']['permissions'],
        )


def test_no_permission(
    all_users: IAllUsers,
    permission_groups: IPermissionGroups,
):
    """Do we get an error if we don't have permission?"""
    with pytest.raises(Forbidden):
        permissions.groups_edit(
            all_users['mods'][0]['token'],
            permission_groups['mod']['group_id'],
            "Renamed",
            permission_groups['mod']['permissions'],
        )


def test_permissions_edited(
    all_users: IAllUsers,
    permission_groups: IPermissionGroups,
):
    """Can users whose permission group was changed do new things?"""
    # Let moderators edit permission groups
    perms = permission_groups['mod']['permissions']
    # I don't like the fact that I have to do this in a loop either, but it's
    # not my fault that JSON is bad
    for p in perms:
        if p['permission_id'] == Permission.ManagePermissionGroups.value:
            p['value'] = True
    permissions.groups_edit(
        all_users['admins'][0]['token'],
        permission_groups['mod']['group_id'],
        permission_groups['mod']['name'],
        perms,
    )
    # They should now be able to do so without errors
    permissions.groups_edit(
        all_users['mods'][0]['token'],
        permission_groups['mod']['group_id'],
        "Renamed",
        permission_groups['mod']['permissions'],
    )


def test_group_name_updated(
    all_users: IAllUsers,
    permission_groups: IPermissionGroups,
):
    """Does the name of a permission group we edited get updated?"""
    permissions.groups_edit(
        all_users['admins'][0]['token'],
        permission_groups['mod']['group_id'],
        "Renamed",
        permission_groups['mod']['permissions'],
    )
    new_groups = permissions.groups_list(
        all_users['admins'][0]['token'])['groups']
    # Make sure it got renamed
    assert len(list(filter(
        lambda g: g['name'] == "Renamed",
        new_groups
    ))) == 1
