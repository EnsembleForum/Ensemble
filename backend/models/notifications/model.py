"""
# Backend / Models / Notifications / Model

Model for notifications.
"""
from datetime import datetime
from ..tables import TNotification
from ..user import User
from ..post import Post
from ..comment import Comment
from ..reply import Reply
from ..queue import Queue
from . import NotificationType
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.types.identifiers import NotificationId
from backend.types.notifications import INotificationInfo
from typing import cast, Optional, final


NOTIF_BODY_LEN = 50


def string_shorten(s: str, max_len: int) -> str:
    if len(s) > max_len:
        return s[:max_len-3] + '...'
    return s


class Notification:
    """
    Represents a notification.

    Note that the various kinds of notifications are encapsulated using
    subclasses which provide a function that gives notification info.

    ## Creating a notification type

    1. Subclass this type (for consistency, name it as `NotificationXyz` where
       `Xyz` is the type of notification).
    2. Define the `create` classmethod to only accept info required for that
       type of notification. It should call the `_create` classmethod with all
       required info to create an entry in the database.
    3. Define the `get_info` method to return info about the notification.
    4. Create an enum entry for the notification type.
    5. Create a mapping from the notification type to the new subclass in
       `./mappings.py`, so that the class can be instantiated from the database
       correctly.

    ## Checking the type of a notification

    Even for notifications loaded from the database, subclasses will
    automatically be applied.

    ```py
    notif = Notification(commented_notification_id)
    assert isinstance(notif, NotificationCommented)
    ```
    """
    def __new__(
        cls: type['Notification'],
        id: NotificationId,
    ) -> 'Notification':
        # We if it's a subclass, continue constructing it
        if cls is not Notification:
            return object.__new__(cls)
        # Otherwise, we need to figure out which kind of notification subclass
        # to construct
        row = get_by_id(TNotification, id)
        notif_type = NotificationType(row.notif_type)
        # Use the mappings to instantiate the required subclass
        from .mappings import mappings
        return mappings[notif_type](id)

    def __init__(self, id: NotificationId):
        """
        Create a notification object shadowing an existing notification in the
        database

        ### Args:
        * `id` (`int`): notification id

        ### Raises:
        * `BadRequest`: notification does not exist
        """
        assert_id_exists(TNotification, id)
        self.__id = id

    @classmethod
    def _create(
        cls,
        user_to: User,
        notif_type: NotificationType,
        user_from: Optional[User] = None,
        post: Optional[Post] = None,
        comment: Optional[Comment] = None,
        reply: Optional[Reply] = None,
        queue: Optional[Queue] = None,
    ) -> NotificationId:
        """
        Create a new notification in the database.

        This should be wrapped around by subclasses to provide simpler
        functionality.

        ### Args:
        * `user_to` (`User`): user to send the notification to

        * `notify_type` (`NotificationType`): type of notification

        * `user_from` (`Optional[User]`, optional): user the notification was
          sent from. Defaults to `None`.

        * `post` (`Optional[Post]`, optional): post associated with
          notification. Defaults to `None`.

        * `comment` (`Optional[Comment]`, optional): comment associated with
          notification. Defaults to `None`.

        * `reply` (`Optional[Reply]`, optional): reply associated with
          notification. Defaults to `None`.

        * `queue` (`Optional[Queue]`, optional): queue associated with
          notification. Defaults to `None`.

        ### Returns:
        * `NotificationId`: ID of new notification
        """
        val = TNotification(
            {
                TNotification.user_to: user_to.id,
                TNotification.notif_type: notif_type.value,
                TNotification.user_from: (
                    user_from.id if user_from is not None else None),
                TNotification.post: post.id if post is not None else None,
                TNotification.comment: (
                    comment.id if comment is not None else None),
                TNotification.reply: reply.id if reply is not None else None,
                TNotification.seen: False,
                TNotification.queue: queue.id if queue is not None else None,
                TNotification.timestamp: datetime.now(),
            }
        ).save().run_sync()[0]
        return cast(NotificationId, val["id"])

    @classmethod
    def all(self, user: User) -> list['Notification']:
        """
        Returns a list of notifications for a user
        """
        notifs = TNotification.objects()\
            .where(TNotification.user_to == user.id)\
            .order_by(TNotification.id, ascending=False)\
            .run_sync()
        return [Notification(n.id) for n in notifs]

    def _get(self) -> TNotification:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TNotification, self.__id)

    @property
    def id(self) -> NotificationId:
        """
        The ID of this notification
        """
        return self.__id

    @property
    def user_to(self) -> User:
        """
        The user this notification is directed to
        """
        return User(self._get().user_to)

    @property
    def seen(self) -> bool:
        """
        Whether this notification has been seen or not
        """
        return self._get().seen

    @seen.setter
    def seen(self, new_val: bool):
        row = self._get()
        row.seen = new_val
        row.save().run_sync()

    @property
    def timestamp(self) -> int:
        """
        Time when the notification was sent
        """
        return int(self._get().timestamp.timestamp())

    @property
    def _user_from(self) -> Optional[User]:
        """
        The user this notification was sent from

        This method is private and should only be accessed by subclasses.
        """
        if (user_id := self._get().user_from) is not None:
            return User(user_id)
        else:
            return None

    @property
    def _post(self) -> Optional[Post]:
        """
        Post associated with the notification

        This method is private and should only be accessed by subclasses.
        """
        if (post_id := self._get().post) is not None:
            return Post(post_id)
        else:
            return None

    @property
    def _comment(self) -> Optional[Comment]:
        """
        Comment associated with the notification

        This method is private and should only be accessed by subclasses.
        """
        if (comment_id := self._get().comment) is not None:
            return Comment(comment_id)
        else:
            return None

    @property
    def _reply(self) -> Optional[Reply]:
        """
        Reply associated with the notification

        This method is private and should only be accessed by subclasses.
        """
        if (reply_id := self._get().reply) is not None:
            return Reply(reply_id)
        else:
            return None

    @property
    def _queue(self) -> Optional[Queue]:
        """
        Queue associated with the notification

        This method is private and should only be accessed by subclasses.
        """
        if (queue_id := self._get().queue) is not None:
            return Queue(queue_id)
        else:
            return None

    @final
    def get_info(self) -> INotificationInfo:
        """
        Returns information about the notification

        This wrapper is in-place to trim body text to ensure it's readable on
        the frontend.
        """
        info = self._get_info()
        info['body'] = string_shorten(info['body'], NOTIF_BODY_LEN)
        return info

    def _get_info(self) -> INotificationInfo:
        """
        Returns information about the notification.

        This should be implemented by all subclasses
        """
        raise NotImplementedError("This needs to be implemented by a subclass")
