"""
# Tests / Integration / Admin / Permissions / List permissions test

Tests to ensure list permissions is working

* All permissions are returned
"""
from backend.models.permissions.permission import Permission
from tests.integration.request.admin.permissions import list_permissions
from tests.integration.conftest import IBasicServerSetup


def test_all_permissions_listed(basic_server_setup: IBasicServerSetup):
    """Are all permissions listed?"""
    perms = list_permissions(basic_server_setup['token'])['permissions']
    for p in Permission:
        f = list(filter(lambda c: c['permission_id'] == p.value, perms))
        # It should only be here once and the name should match
        assert len(f) == 1
        assert f[0]['name'] == p.name
