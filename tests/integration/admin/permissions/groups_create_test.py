"""
# Tests / Integration / Admin / Permissions / Groups create

Tests for creating permission groups

* Group name already taken
* Group name empty
* Don't have `ManageUserGroups` permission
* Group doesn't contain all available permissions
* Group created
"""
import pytest
from tests.integration.conftest import IBasicServerSetup, IAllUsers
from tests.integration.request.admin import permissions
from backend.util.http_errors import BadRequest
from backend.models.permissions import Permission
from backend.types.permissions import IPermissionGroup, PermissionGroupId


def test_duplicate_group_name(basic_server_setup: IBasicServerSetup):
    """Do we fail to create a group if it's got a duplicate name?"""
    with pytest.raises(BadRequest):
        permissions.groups_create(
            basic_server_setup['token'],
            'Administrator',
            [
                {"permission_id": p.value, "value": False}
                for p in Permission
            ],
        )


def test_empty_group_name(basic_server_setup: IBasicServerSetup):
    """Do we fail to create a group if it's got an empty name?"""
    with pytest.raises(BadRequest):
        permissions.groups_create(
            basic_server_setup['token'],
            '',
            [
                {"permission_id": p.value, "value": False}
                for p in Permission
            ],
        )


def test_no_permission(all_users: IAllUsers):
    """Do we fail to create a group if we don't have permission?"""
    with pytest.raises(BadRequest):
        permissions.groups_create(
            all_users['mods'][0]['token'],
            'My group',
            [
                {"permission_id": p.value, "value": False}
                for p in Permission
            ],
        )


def test_not_all_values(basic_server_setup: IBasicServerSetup):
    """Do we fail to create a group if we don't specify all permission values?
    """
    with pytest.raises(BadRequest):
        permissions.groups_create(
            basic_server_setup['token'],
            'My group',
            [],
        )


def test_success(basic_server_setup: IBasicServerSetup):
    """Can we create a permission group successfully?"""
    group_properties: IPermissionGroup = {
        "group_id": PermissionGroupId(-1),
        "name": "My group",
        "permissions": [
            {"permission_id": p.value, "value": False}
            for p in Permission
        ],
    }
    group_properties["group_id"] = permissions.groups_create(
        basic_server_setup['token'],
        group_properties["name"],
        group_properties["permissions"],
    )["group_id"]
    # Check the group exists
    groups = permissions.groups_list(basic_server_setup['token'])['groups']
    assert len(groups) == 4
    assert group_properties in groups
