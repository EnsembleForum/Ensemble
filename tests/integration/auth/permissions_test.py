"""
# Tests / Integration / Auth / Permissions test

Check that permissions callback works correctly.

* Do we get given the right permissions?
* If we edit a user's permissions is that reflected?
"""
import pytest
from typing import cast
from ..conftest import IBasicServerSetup, ISimpleUsers
from backend.types.permissions import IPermissionValueUser
from ensemble_request.auth import permissions
from ensemble_request.admin.permissions import set_permissions, get_permissions


@pytest.mark.core
def test_correct_permissions(basic_server_setup: IBasicServerSetup):
    """Do we get given the right permissions?"""
    # Admins should have all permissions
    assert all(
        map(
            lambda p: p['value'],
            permissions(basic_server_setup['token'])['permissions'],
        )
    )


def test_update_permissions(simple_users: ISimpleUsers):
    """If we edit a user's permissions is that reflected?"""
    # Make the user have all the permissions of the admin
    set_permissions(
        simple_users['admin']['token'],
        simple_users['user']['user_id'],
        # This is actually type-safe, since IPermissionValueGroup is compatible
        # with IPermissionValueUser - I can't think of a nicer way to do this
        cast(list[IPermissionValueUser], simple_users['admin']['permissions']),
        # Maybe we should return their permission group ID too - this lookup is
        # kinda pain
        get_permissions(
            simple_users['admin']['token'],
            simple_users['user']['user_id'],
        )['group_id'],
    )
    # Now make sure they have every permission
    assert all(
        map(
            lambda p: p['value'],
            permissions(simple_users['user']['token'])['permissions'],
        )
    )
