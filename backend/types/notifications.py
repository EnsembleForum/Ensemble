"""
# Backend / Types / Notifications

Types used within notifications
"""
from typing import TypedDict, Optional
from .identifiers import NotificationId, PostId, CommentId, ReplyId, QueueId


class INotificationInfo(TypedDict):
    """
    Information for a notification

    * `notification_id` (`int`): ID of notification
    * `heading` (`str`): Heading of notification text
    * `body` (`str`): Body of notification text
    * `post` (`int`, optional): ID of post related to notification
    * `comment` (`int`, optional): ID of comment related to notification. If
      this property is non-null, then `post` will also be defined.
    * `reply` (`int`, optional): ID of reply related to the notification. If
      this property is non-null, then `comment` and `post` will also be
      defined.
    * `queue` (`int`, optional): ID of queue related to the notification
    """
    notification_id: NotificationId
    heading: str
    body: str
    post: Optional[PostId]
    comment: Optional[CommentId]
    reply: Optional[ReplyId]
    queue: Optional[QueueId]


class INotificationList(TypedDict):
    """
    List of notifications.

    * `notifications`: list of objects, each containing:
            * `notification_id` (`int`): ID of notification
            * `heading` (`str`): Heading of notification text
            * `body` (`str`): Body of notification text
            * `post` (`int`): ID of post related to notification
            * `comment` (`int`): ID of comment related to notification. If this
            property is non-null, then `post` will also be defined.
            * `reply` (`int`): ID of reply related to the notification. If this
            property is non-null, then `comment` and `post` will also be
            defined.
    """
    notifications: list[INotificationInfo]
