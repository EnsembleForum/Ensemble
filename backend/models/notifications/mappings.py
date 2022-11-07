"""
# Models / Notifications / Mappings

Mappings between notification type and notification subclass
"""
from .notification_type import NotificationType
from .types import (
    NotificationCommented,
    NotificationClosed
)


mappings = {
    NotificationType.Commented: NotificationCommented,
    NotificationType.Closed: NotificationClosed,
}
