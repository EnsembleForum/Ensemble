"""
# Tests / Integration / Admin / Permissions / Groups list

Tests for listing permission groups

* Are the three default groups created, and do they contain all the required
  keys?
* Does the administrator group have every permission?
* Do we get an error if we don't have permission?
"""
import pytest
from tests.integration.conftest import IBasicServerSetup, IAllUsers
from request.admin import permissions
from backend.models.permissions.permission import Permission
from backend.util.http_errors import Forbidden


def test_default_groups(basic_server_setup: IBasicServerSetup):
    """
    Are the three default groups created, and do they contain all the required
    keys?
    """
    # Default group names
    defaults = {
        1: "Administrator",
        2: "Moderator",
        3: "User",
    }
    groups = permissions.groups_list(basic_server_setup['token'])['groups']
    assert len(groups) == 3
    for g in groups:
        # Make sure the name and ID are correct
        assert defaults[g['group_id']] == g['name']
        # Make sure all permissions are defined
        # We don't check that permissions have the correct values, but they
        # need to at least be defined
        for p in Permission:
            assert len(list(filter(
                lambda gp: gp['permission_id'] == p.value,
                g['permissions']
            ))) == 1
        # Permissions must not be None
        for v in g['permissions']:
            assert v['value'] is not None


def test_admins_have_every_permission(basic_server_setup: IBasicServerSetup):
    """Does the administrator group have every permission"""
    groups = permissions.groups_list(basic_server_setup['token'])['groups']
    for g in groups:
        if g['name'] == 'Administrator':
            # Make sure all permissions are True
            for p in g['permissions']:
                assert p['value'] is True


def test_no_permission(all_users: IAllUsers):
    """Do we get an error if we don't have permission?"""
    with pytest.raises(Forbidden):
        permissions.groups_list(all_users['users'][0]['token'])
