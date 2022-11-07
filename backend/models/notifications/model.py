"""
# Backend / Models / Notifications / Model

Model for notifications.
"""
from ..tables import TNotification
from ..user import User
from ..post import Post
from ..comment import Comment
from ..reply import Reply
from . import NotificationType
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.types.identifiers import NotificationId
from backend.types.notifications import INotificationInfo
from typing import cast, Optional
from abc import abstractmethod


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

        ### Returns:
        * `NotificationId`: ID of new notification
        """
        val = TNotification(
            {
                TNotification.user_to: user_to,
                TNotification.notif_type: notif_type.value,
                TNotification.user_from: user_from,
                TNotification.post: post.id if post is not None else None,
                TNotification.comment: (
                    comment.id if comment is not None else None),
                TNotification.reply: reply.id if reply is not None else None,
                TNotification.viewed: False,
            }
        ).save().run_sync()[0]
        return cast(NotificationId, val["id"])

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
    def viewed(self) -> bool:
        """
        Whether this notification has been viewed or not
        """
        return self._get().viewed

    @viewed.setter
    def viewed(self, new_val: bool):
        row = self._get()
        row.viewed = new_val
        row.save().run_sync()

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

    @abstractmethod
    def get_info(self) -> INotificationInfo:
        """
        Returns information about the notification
        """
