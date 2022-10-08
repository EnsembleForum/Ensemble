"""
# Backend / Routes / Admin

Contains route definitions for functions used with administration
"""
from flask import Blueprint
from .permissions import permissions
from .users import users


admin = Blueprint('admin', 'admin')

admin.register_blueprint(permissions, url_prefix='/permissions')
admin.register_blueprint(users, url_prefix='/users')


@admin.get('/is_first_run')
def is_first_run():
    """Returns whether the datastore is empty"""


__all__ = [
    'admin',
]
