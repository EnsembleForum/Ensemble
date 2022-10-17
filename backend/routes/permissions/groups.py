"""
# Backend / Routes / Permissions / Groups

Routes for managing permission groups
"""
from flask import Blueprint


groups = Blueprint('groups', 'permissions.groups')


@groups.post('/create')
def create():
    return {}


@groups.get('/list')
def list():
    return {}


@groups.put('/edit')
def edit():
    return {}


@groups.delete('/remove')
def remove():
    return {}
