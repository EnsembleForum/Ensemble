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
from backend.models.permissions.permission import Permission


def test_duplicate_group_name(basic_server_setup: IBasicServerSetup):
    """Do we fail to create a group if it's got a duplicate name?"""
    with pytest.raises(BadRequest):
        permissions.groups_create(
            basic_server_setup['token'],
            'Administrator',
            {
                p.value: False
                for p in Permission
            },
        )


def test_empty_group_name(basic_server_setup: IBasicServerSetup):
    """Do we fail to create a group if it's got an empty name?"""
    with pytest.raises(BadRequest):
        permissions.groups_create(
            basic_server_setup['token'],
            '',
            {
                p.value: False
                for p in Permission
            },
        )


def test_no_permission(all_users: IAllUsers):
    """Do we fail to create a group if we don't have permission?"""
    with pytest.raises(BadRequest):
        permissions.groups_create(
            all_users['mods'][0]['token'],
            'My group',
            {
                p.value: False
                for p in Permission
            },
        )


def test_not_all_values(basic_server_setup: IBasicServerSetup):
    """Do we fail to create a group if we don't specify all permission values?
    """
    with pytest.raises(BadRequest):
        permissions.groups_create(
            basic_server_setup['token'],
            'My group',
            {},
        )


def test_success(basic_server_setup: IBasicServerSetup):
    """Can we create a permission group successfully?"""
    group = permissions.groups_create(
        basic_server_setup['token'],
        'My group',
        {
            p.value: False
            for p in Permission
        },
    )
    # Check the group exists
    # TODO
    del group
