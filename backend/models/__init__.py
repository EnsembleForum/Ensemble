"""
# Backend / Models

Contains code for the data structures used internally by the backend.
"""
from .permissions.permission import Permission
from .permissions.permission_set import PermissionUser, PermissionGroup
from .user import User
from .post import Post
from .comment import Comment
from .reply import Reply
from .token import Token
from .auth_config import AuthConfig
from .analytics import Analytics
from .notifications import Notification
from .exam_mode import ExamMode
from .queue import Queue
from .tag import Tag


# Initialise the database
from . import piccolo_app
from . import tables
del piccolo_app
del tables


__all__ = [
    'Permission',
    'PermissionGroup',
    'PermissionUser',
    'User',
    'Post',
    'Comment',
    'Reply',
    'Token',
    'AuthConfig',
    'Analytics',
    'Notification',
    'ExamMode',
    'Queue',
    'Tag',
]
