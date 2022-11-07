"""
# Backend / Routes / Notifications

Notification routes
"""
import json
from flask import Blueprint, request
from backend.util import http_errors
from backend.models.notifications import Notification
from backend.models.user import User
from backend.util.tokens import uses_token
from backend.types.identifiers import NotificationId
from backend.types.notifications import INotificationList


notifications = Blueprint('notifications', 'notifications')


@notifications.get('/list')
@uses_token
def list_notifs(user: User, *_) -> INotificationList:
    return {
        "notifications": list(map(
            lambda n: n.get_info(),
            Notification.all(user),
        ))
    }


@notifications.put('/seen')
@uses_token
def seen(user: User, *_) -> dict:
    data = json.loads(request.data)
    notif = Notification(NotificationId(data["notification_id"]))
    seen: bool = data["seen"]
    if notif.user_to != user:
        raise http_errors.Forbidden("Cannot see notifications not belonging "
                                    "to user")
    notif.seen = seen
    return {}
