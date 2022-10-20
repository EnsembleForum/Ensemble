"""
# Backend / Models / Permissions / Permission

Contains definitions for permissions that can be granted to users.
"""
from enum import Enum
from typing import cast
from backend.types.identifiers import PermissionId


class Permission(Enum):
    """
    Enum containing definitions for all the permission types of users.
    """
    @property
    def value(self) -> PermissionId:
        return cast(PermissionId, super().value)

    # Viewing
    View = 0
    """User can view public posts"""
    ViewPrivate = 1
    """User can view private posts"""
    ViewAnonymousOP = 2
    """User can view who made an anonymous post"""

    # Posting
    Post = 10
    """User can create posts"""
    Answer = 11
    """User can create answers to posts"""
    PostOverrideExam = 12
    """User can create public posts, even when exam mode is enabled"""

    # Taskboard and queues
    ViewTaskboard = 20
    """User can view the taskboard overview"""
    Delegate = 21
    """User can move a post from the main queue to a specialised queue"""
    FollowQueue = 22
    """User can subscribe to queues to get notifications when posts are moved
    into them"""

    # Moderation
    ReportPosts = 30
    """User can report posts to get them reviewed by a moderator"""
    ClosePosts = 31
    """User can close posts to give feedback before the post is reopened"""
    DeletePosts = 32
    """User can delete posts to prevent them from being reopened"""
    ViewReports = 33
    """User can view the list of reported posts"""

    # User management
    ManageUserPermissions = 40
    """User can set the permission level of other users"""
    AddUsers = 41
    """User can create other user accounts"""
    RemoveUsers = 42
    """User can remove other user accounts"""
    ViewAllUsers = 43
    """User can view the list of users"""

    # Administration
    ManageAuthConfig = 50
    """User can manage authentication options"""
    ManagePermissionGroups = 51
    """manage permissions groups, including creation, deletion and modification
    """
