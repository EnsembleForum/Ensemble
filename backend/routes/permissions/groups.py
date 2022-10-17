"""
# Backend / Routes / Permissions / Groups

Routes for managing permission groups
"""
from flask import Blueprint
from backend.types.identifiers import PermissionGroupId
from backend.types.permissions import IGroupId, IPermissionGroupList


groups = Blueprint('groups', 'permissions.groups')


@groups.post('/create')
def create() -> IGroupId:
    return {
        "group_id": PermissionGroupId(0),
    }


@groups.get('/list')
def list() -> IPermissionGroupList:
    return {
        "groups": []
    }


@groups.put('/edit')
def edit() -> dict:
    return {}


@groups.delete('/remove')
def remove() -> dict:
    return {}
