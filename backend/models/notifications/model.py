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
from typing import cast, Optional


class Notification:
    """
    Represents a notification
    """
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
    def create(
        cls,
        user_to: User,
        notify_type: NotificationType,
        user_from: Optional[User] = None,
        post: Optional[Post] = None,
        comment: Optional[Comment] = None,
        reply: Optional[Reply] = None,
    ) -> 'Notification':
        """
        Create a new notification

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
        * `Notification`: new notification
        """
        val = TNotification(
            {
                TNotification.user_to: user_to,
                TNotification.notify_type: notify_type.value,
                TNotification.user_from: user_from,
                TNotification.post: post.id if post is not None else None,
                TNotification.comment: (
                    comment.id if comment is not None else None),
                TNotification.reply: reply.id if reply is not None else None
            }
        ).save().run_sync()[0]
        id = cast(NotificationId, val["id"])
        return Notification(id)

    def _get(self) -> TNotification:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TNotification, self.__id)

    @property
    def notify_type(self) -> NotificationType:
        """
        The type of the notification
        """
        return NotificationType(self._get().notify_type)

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
    def user_from(self) -> Optional[User]:
        """
        The user this notification was sent from
        """
        if (user_id := self._get().user_from) is not None:
            return User(user_id)
        else:
            return None

    @property
    def post(self) -> Optional[Post]:
        if (post_id := self._get().post) is not None:
            return Post(post_id)
        else:
            return None

    @property
    def comment(self) -> Optional[Comment]:
        if (comment_id := self._get().comment) is not None:
            return Comment(comment_id)
        else:
            return None

    @property
    def reply(self) -> Optional[Reply]:
        if (reply_id := self._get().reply) is not None:
            return Reply(reply_id)
        else:
            return None
