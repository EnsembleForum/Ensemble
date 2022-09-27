"""
# Backend / Routes

Contains definitions for all routes used by the backend
"""
# Keep flake8 happy
__all__ = [
    'debug',
]

from .debug import blueprint as debug
