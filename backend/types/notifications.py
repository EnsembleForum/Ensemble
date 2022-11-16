"""
# Backend / Types / Notifications

Types used within notifications
"""
from typing import TypedDict, Optional
from .identifiers import (
    NotificationId,
    UserId,
    PostId,
    CommentId,
    ReplyId,
    QueueId,
)


class INotificationInfo(TypedDict):
    """
    Information for a notification

    * `notification_id` (`int`): ID of notification
    * `user_from` (`int`, optional): user ID of person who sent the
      notification, or null if the action was anonymous
    * `seen` (`bool`): whether the post has been seen
    * `timestamp` (`int`): the time when the notification was sent
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
    user_from: Optional[UserId]
    seen: bool
    timestamp: int
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
            * `seen` (`bool`): whether the post has been seen
            * `user_from` (`int`, optional): user ID of person who sent the
              notification, or null if the action was anonymous
            * `heading` (`str`): Heading of notification text
            * `body` (`str`): Body of notification text
            * `post` (`int`, optional): ID of post related to notification
            * `comment` (`int`, optional): ID of comment related to
              notification. If this property is non-null, then `post` will also
              be defined.
            * `reply` (`int`, optional): ID of reply related to the
              notification. If this property is non-null, then `comment` and
              `post` will also be defined.
            * `queue` (`int`, optional): ID of queue related to the
              notification.
    """
    notifications: list[INotificationInfo]
