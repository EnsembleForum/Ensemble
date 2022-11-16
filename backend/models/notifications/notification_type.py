"""
# Backend / Models / Notifications / Enum

Enum representing post types
"""
from enum import Enum


class NotificationType(Enum):
    Commented = 0
    """Someone commented on your post, or replied to your comment"""

    Reacted = 10
    """Someone reacted to your post/comment/reply"""

    Closed = 20
    """Mod closed your post"""
    Deleted = 21
    """Mod deleted your post/comment/reply"""

    Accepted = 30
    """Your answer got accepted"""
    Unaccepted = 31
    """Your answer got unaccepted"""

    QueueAdded = 40
    """Post added to a queue you follow"""

    Reported = 50
    """A post got reported"""
