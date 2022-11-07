"""
# Backend / Models / Notifications / Types

Logic for specific types of notifications
"""
from .commented import NotificationCommented
from .closed import NotificationClosed


__all__ = [
    'NotificationCommented',
    'NotificationClosed',
]
