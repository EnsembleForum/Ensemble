"""
# Request

Contains code used for requesting routes available on the backend. This is used
for testing, and for generating documentation of the available routes.
"""
from . import (
    admin,
    auth,
    browse,
    debug,
    user,
)

__all__ = [
    'admin',
    'auth',
    'browse',
    'debug',
    'user',
]
