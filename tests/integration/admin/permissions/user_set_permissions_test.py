"""
# Tests / Integration / Admin / Permissions / User set permissions test

Tests for setting the specific permissions of users.

* Not all permissions set
* User ID not valid
* Group ID not valid
* Changing your own permissions
* Don't have ManageUserPermissions permission
* Permission groups can change
* Can set individual permissions
"""
import pytest
from ensemble_request.admin.permissions import (
    get_permissions,
    set_permissions,
)
from tests.integration.conftest import (
    ISimpleUsers,
    IBasicServerSetup,
    IPermissionGroups,
)
from backend.models.permissions.permission import Permission
from backend.util.http_errors import Forbidden, BadRequest
from backend.types.identifiers import UserId, PermissionGroupId


def test_not_all_permissions_set(
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """If we don't give info on all permissions, do we get an error?"""
    with pytest.raises(BadRequest):
        set_permissions(
            simple_users['admin']['token'],
            simple_users['mod']['user_id'],
            [],
            permission_groups['user']['group_id'],
        )


def test_user_id_invalid(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """Do we get an error if we try to set permissions for an invalid user?"""
    with pytest.raises(BadRequest):
        set_permissions(
            basic_server_setup['token'],
            UserId(-1),
            [{"permission_id": p.value, "value": None} for p in Permission],
            permission_groups['user']['group_id'],
        )


def test_group_id_invalid(simple_users: ISimpleUsers):
    """Do we get an error if we try to set permissions for an invalid group?"""
    with pytest.raises(BadRequest):
        set_permissions(
            simple_users['admin']['token'],
            simple_users['mod']['user_id'],
            [{"permission_id": p.value, "value": None} for p in Permission],
            PermissionGroupId(-1),
        )


def test_set_own_permission_id(
    basic_server_setup: IBasicServerSetup,
    permission_groups: IPermissionGroups,
):
    """Do we get an error if we try to our own permissions?"""
    with pytest.raises(BadRequest):
        set_permissions(
            basic_server_setup['token'],
            basic_server_setup['user_id'],
            [{"permission_id": p.value, "value": None} for p in Permission],
            permission_groups['user']['group_id'],
        )


def test_no_permission(
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """
    Do we get an error if we don't have permission to set a user's permissions?
    """
    with pytest.raises(Forbidden):
        set_permissions(
            simple_users['mod']['token'],
            simple_users['admin']['user_id'],
            [{"permission_id": p.value, "value": None} for p in Permission],
            permission_groups['user']['group_id'],
        )


def test_change_permission_group(
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """Can we change the permission group of a person?"""
    set_permissions(
        simple_users['admin']['token'],
        simple_users['user']['user_id'],
        [{"permission_id": p.value, "value": None} for p in Permission],
        permission_groups['mod']['group_id'],
    )
    perms = get_permissions(
        simple_users['admin']['token'],
        simple_users['user']['user_id']
    )
    assert perms['group_id'] == permission_groups['mod']['group_id']
    for v in perms['permissions']:
        assert v['value'] is None


@pytest.mark.core
@pytest.mark.parametrize(
    'value',
    [True, False]
)
def test_change_permissions_true(
    value: bool,
    simple_users: ISimpleUsers,
    permission_groups: IPermissionGroups,
):
    """Can we change the permissions of a person?"""
    set_permissions(
        simple_users['admin']['token'],
        simple_users['user']['user_id'],
        [{"permission_id": p.value, "value": value} for p in Permission],
        permission_groups['user']['group_id'],
    )
    perms = get_permissions(
        simple_users['admin']['token'],
        simple_users['user']['user_id']
    )
    assert perms['group_id'] == permission_groups['user']['group_id']
    for v in perms['permissions']:
        assert v['value'] is value
