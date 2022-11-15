"""
# Models / Notifications / Mappings

Mappings between notification type and notification subclass
"""
from .notification_type import NotificationType
from .model import Notification
from .types import (
    NotificationAccepted,
    NotificationClosed,
    NotificationCommented,
    NotificationDeleted,
    NotificationQueueAdded,
    NotificationReacted,
    NotificationReported,
    NotificationUnaccepted,
)


mappings: dict[NotificationType, type[Notification]] = {
    NotificationType.Accepted: NotificationAccepted,
    NotificationType.Commented: NotificationCommented,
    NotificationType.Closed: NotificationClosed,
    NotificationType.Deleted: NotificationDeleted,
    NotificationType.QueueAdded: NotificationQueueAdded,
    NotificationType.Reacted: NotificationReacted,
    NotificationType.Unaccepted: NotificationUnaccepted,
    NotificationType.Reported: NotificationReported,
}
