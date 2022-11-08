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

    FIXME: Currently the docstrings for each permission cannot be accessed by
    the script generate_permissions script. If we want to give descriptions for
    each permission to our users, we need a better way to store this.
    """
    @property
    def value(self) -> PermissionId:
        return cast(PermissionId, super().value)

    # Viewing
    PostView = 0
    """User can view public posts"""
    ViewPrivate = 1
    """User can view private posts"""
    ViewAnonymousOP = 2
    """User can view who made an anonymous post"""

    # Posting
    PostCreate = 10
    """User can create posts"""
    PostComment = 11
    """User can create answers to posts"""
    PostOverrideExam = 12
    """User can create public posts, even when exam mode is enabled"""

    # Comments
    CommentAccept = 13
    """Non-OP user can mark a comment as accepted"""

    # Taskboard and queues
    ViewTaskboard = 20
    """User can view the taskboard overview"""
    TaskboardDelegate = 21
    """User can move a post from the main queue to a specialised queue"""
    FollowQueue = 22
    """User can subscribe to queues to get notifications when posts are moved
    into them"""
    ManageQueues = 23
    """User can manage taskboard queues, including creating and deleting them.
    """

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
    """User can manage permissions groups, including creation, deletion and
    modification
    """
    
    # Exam mode
    SetExamMode = 52
    """User can turn on or off exam mode"""
