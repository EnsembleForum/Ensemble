"""
# Ensemble request / Notifications

Requests for getting notifications
"""
from typing import cast
from backend.types.auth import JWT
from backend.types.identifiers import NotificationId
from backend.types.notifications import INotificationList
from .consts import URL
from .helpers import get, put

URL = f"{URL}/notifications"


def list(token: JWT) -> INotificationList:
    """
    ## GET `/notifications/list`

    Returns a list of notifications for a user

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Returns
    Object containing:
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
    return cast(
        INotificationList,
        get(
            token,
            f"{URL}/list",
            {},
        )
    )


def seen(token: JWT, notification_id: NotificationId, value: bool):
    """
    ## PUT `/notifications/seen`

    Updates whether a particular notification has been seen or not

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `notification_id` (`int`): ID of the notification
    * `value` (`bool`): whether the notification should count as seen or not

    ## Errors
    * `BadRequest`: invalid notification ID
    * `Forbidden`: cannot see notifications not belonging to user

    ## Errors

    ### 400
    * Invalid notification ID

    ### 403
    * Cannot see notifications belonging to another user
    """
    put(
        token,
        f"{URL}/seen",
        {
            "notification_id": notification_id,
            "value": value,
        }
    )
