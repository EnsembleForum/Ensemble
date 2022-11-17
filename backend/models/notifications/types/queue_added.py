"""
# Backend / Models / Notifications / Types / Queue added

Notification for "A new post was added to a queue you follow"
"""
from backend.models.post import Post
from backend.models.queue import Queue
from .. import NotificationType
from .. import Notification
from ...user import User
from backend.types.notifications import INotificationInfo


class NotificationQueueAdded(Notification):
    """
    Notification for "A new post was added to a queue you follow"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        user_from: User,
        post: Post,
        queue: Queue,
    ) -> 'NotificationQueueAdded':
        """
        Create a notification that a post was added to a queue you follow

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `user_from` (`User`): user who wrote the comment/reply

        * `ref` (`Comment | Reply`): reference to the comment/reply

        ### Returns:
        * `NotificationCommented`: notification object
        """

        return NotificationQueueAdded(cls._create(
            user_to,
            NotificationType.QueueAdded,
            user_from,
            post,
            queue=queue,
        ))

    @property
    def user_from(self) -> User:
        u = self._user_from
        assert u is not None
        return u

    @property
    def post(self) -> Post:
        p = self._post
        assert p is not None
        return p

    @property
    def queue(self) -> Queue:
        q = self._queue
        assert q is not None
        return q

    def _get_info(self) -> INotificationInfo:
        return {
            "notification_id": self.id,
            "timestamp": self.timestamp,
            "seen": self.seen,
            "user_from": self.user_from.id,
            "heading": f"New post in queue {self.queue.name}",
            "body": self.post.heading,
            "post": self.post.id,
            "comment": None,
            "reply": None,
            "queue": self.queue.id,
        }
