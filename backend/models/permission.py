"""
# Backend / Models / Permission

Contains definitions for permissions that can be granted to users.
"""
from enum import Enum


class Permission(Enum):
    """
    Enum containing definitions for all the permission types of users.
    """
    # Viewing
    View = 0
    """User can view public posts"""
    ViewPrivate = 1
    """User can view private posts"""

    # Posting
    Post = 10
    """User can create posts"""
    Answer = 11
    """User can create answers to posts"""
    PostOverrideExam = 12
    """User can create public posts, even when exam mode is enabled"""

    # Queues
    Delegate = 20
    """User can move a post from the main queue to a specialised queue"""
    FollowQueue = 21
    """User can subscribe to queues to get notifications when a post is moved
    into it"""

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
    SetUserPermissions = 40
    """User can set the permission level of other users"""
    AddUsers = 41
    """User can create other user accounts"""
    RemoveUsers = 42
    """User can remove other user accounts"""
