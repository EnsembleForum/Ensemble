

from enum import Enum


class Permissions(Enum):
    """
    Contains definitions for all the permission types of users.
    """
    # Viewing
    CanView = 0
    """User can view public posts"""
    CanViewPrivate = 1
    """User can view private posts"""

    # Posting
    CanPost = 10
    """User can create posts"""
    CanAnswer = 11
    """User can create answers to posts"""

    # Queues
    CanDelegate = 20
    """User can move a post from the main queue to a specialised queue"""
    CanFollowQueue = 21
    """User can subscribe to queues to get notifications when a post is moved
    into it"""

    # Moderation
    CanReportPosts = 30
    """User can report posts to get them reviewed by a moderator"""
    CanClosePosts = 31
    """User can close posts to give feedback before the post is reopened"""
    CanDeletePosts = 32
    """User can delete posts to prevent them from being reopened"""
    CanViewReports = 33
    """User can view the list of reported posts"""

    # User management
    CanSetUserPermission = 40
    """User can set the permission level of other users"""
    CanAddUsers = 41
    """User can create other user accounts"""
    CanRemoveUsers = 42
    """User can remove other user accounts"""
