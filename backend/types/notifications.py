"""
# Backend / Types / Notifications

Types used within notifications
"""
from typing import TypedDict, Optional
from .identifiers import NotificationId, PostId, CommentId, ReplyId


class INotificationInfo(TypedDict):
    """
    Information for a notification

    * `notification_id` (`int`): ID of notification
    * `heading` (`str`): Heading of notification text
    * `body` (`str`): Body of notification text
    * `post` (`int`): ID of post related to notification
    * `comment` (`int`): ID of comment related to notification. If this
      property is non-null, then `post` will also be defined.
    * `reply` (`int`): ID of reply related to the notification. If this
      property is non-null, then `comment` and `post` will also be defined.
    """
    notification_id: NotificationId
    heading: str
    body: str
    post: Optional[PostId]
    comment: Optional[CommentId]
    reply: Optional[ReplyId]


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
