"""
# Backend / Models / Notifications / Types / Reported

Notification for "Post reported"
"""
from backend.models.post import Post
from .. import NotificationType
from .. import Notification
from ...user import User
from backend.types.notifications import INotificationInfo


class NotificationReported(Notification):
    """
    Notification for "Post reported"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        post: Post,
    ) -> 'NotificationReported':
        """
        Create a notification that a post was reported

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `user_from` (`User`): user who wrote the comment/reply

        * `post` (`Post`): reference to the comment/reply

        ### Returns:
        * `NotificationReported`: notification object
        """

        return NotificationReported(cls._create(
            user_to,
            NotificationType.Reported,
            None,
            post,
        ))

    @property
    def post(self) -> Post:
        p = self._post
        assert p is not None
        return p

    def _get_info(self) -> INotificationInfo:
        return {
            "notification_id": self.id,
            "timestamp": self.timestamp,
            "seen": self.seen,
            "user_from": None,
            "heading": "Post reported",
            "body": self.post.heading,
            "post": self.post.id,
            "comment": None,
            "reply": None,
            "queue": None,
        }
