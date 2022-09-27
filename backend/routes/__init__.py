"""
# Backend / Routes

Contains definitions for all routes used by the backend. These routes should be
structured as blueprints, which can be registered to the server. This helps
keep the code structured and maintainable.
"""
# Keep flake8 happy
__all__ = [
    'debug',
]

from .debug import blueprint as debug
