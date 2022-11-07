"""
# Models / Notifications / Mappings

Mappings between notification type and notification subclass
"""
from .notification_type import NotificationType
from .types import (
    NotificationAccepted,
    NotificationClosed,
    NotificationCommented,
    NotificationDeleted,
    NotificationQueueAdded,
    NotificationReacted,
    NotificationUnaccepted,
)


mappings = {
    NotificationType.Accepted: NotificationAccepted,
    NotificationType.Commented: NotificationCommented,
    NotificationType.Closed: NotificationClosed,
    NotificationType.Deleted: NotificationDeleted,
    NotificationType.QueueAdded: NotificationQueueAdded,
    NotificationType.Reacted: NotificationReacted,
    NotificationType.Unaccepted: NotificationUnaccepted,
}
