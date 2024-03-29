"""
# Backend / Routes

Contains definitions for all routes used by the backend. These routes should be
structured as blueprints, which can be registered to the server. This helps
keep the code structured and maintainable.
"""
# Keep flake8 happy
__all__ = [
    "debug",
    "admin",
    "auth",
    "browse",
    'user',
    'taskboard',
    'notifications',
    'tags',
]

from .debug import debug
from .admin import admin
from .auth import auth
from .browse import browse
from .user import user
from .taskboard import taskboard
from .notifications import notifications
from .tags import tags
