"""
# Backend / Routes / Permissions / Groups

Routes for managing permission groups
"""
import json
from flask import Blueprint, request
from backend.types.identifiers import PermissionGroupId
from backend.types.permissions import (
    IGroupId,
    IPermissionGroupList,
    IPermissionValueGroup,
)
from backend.models import (
    PermissionGroup,
    Permission,
    User,
)
from backend.models.permissions import map_permissions_group
from backend.util.tokens import uses_token
from backend.util.http_errors import BadRequest


groups = Blueprint('groups', 'groups')


@groups.post('/create')
@uses_token
def create(user: User, *_) -> IGroupId:
    user.permissions.assert_can(Permission.ManagePermissionGroups)
    data = json.loads(request.data)
    name: str = data['name']
    permissions: list[IPermissionValueGroup] = data['permissions']
    if PermissionGroup.from_name(name) is not None:
        raise BadRequest(f"A permission group with name {name} already exists")
    mapped_perms = map_permissions_group(permissions)
    group = PermissionGroup.create(name, mapped_perms, False)
    return {
        "group_id": group.id
    }


@groups.get('/list')
@uses_token
def list_groups(user: User, *_) -> IPermissionGroupList:
    user.permissions.assert_can(Permission.ManagePermissionGroups)
    groups = PermissionGroup.all()
    return {"groups": [
        {
            "group_id": g.id,
            "name": g.name,
            "permissions": [
                {
                    "permission_id": p.value,
                    "value": g.can(p),
                }
                for p in Permission
            ]
        }
        for g in groups
    ]}


@groups.put('/edit')
@uses_token
def edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.ManagePermissionGroups)
    data = json.loads(request.data)
    group = PermissionGroup(PermissionGroupId(data['group_id']))
    name: str = data['name']
    permissions: list[IPermissionValueGroup] = data['permissions']

    if (duplicate := PermissionGroup.from_name(name)) is not None:
        # Only if it's not this group
        if duplicate.id != group.id:
            raise BadRequest(
                f"A permission group with name {name} already exists")

    if group.immutable:
        raise BadRequest("Cannot edit immutable groups")

    group.name = name
    group.update_allowed(map_permissions_group(permissions))
    return {}


@groups.delete('/remove')
@uses_token
def remove(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.ManagePermissionGroups)
    group = PermissionGroup(PermissionGroupId(int(request.args['group_id'])))
    transfer_group = PermissionGroup(
        PermissionGroupId(int(request.args['transfer_group_id'])))

    # Make sure we're not just transferring users to the same group
    if group == transfer_group:
        raise BadRequest(
            "Cannot transfer users to same group when deleting a group")

    if group.immutable:
        raise BadRequest("Cannot remove immutable groups")

    # Find users in group to delete, and transfer them to the transfer group
    for u in group.get_users():
        u.permissions.parent = transfer_group
    group.delete()
    return {}
