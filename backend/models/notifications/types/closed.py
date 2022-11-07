"""
# Backend / Models / Notifications / Types / Closed

Notification for "A moderator closed your post"
"""
from backend.models.post import Post
from .. import NotificationType
from .. import Notification
from ...user import User
from backend.types.notifications import INotificationInfo


class NotificationClosed(Notification):
    """
    Notification for "A moderator closed your post"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        post: Post,
    ) -> 'NotificationClosed':
        """
        Create a notification that someone closed your post

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `post` (`Post`): reference to the post that was closed

        ### Returns:
        * `NotificationCommented`: notification object
        """

        return NotificationClosed(cls._create(
            user_to,
            NotificationType.Closed,
            post=post,
        ))

    @property
    def post(self) -> Post:
        p = self._post
        assert p is not None
        return p

    def get_info(self) -> INotificationInfo:
        return {
            "notification_id": self.id,
            "heading": f"A moderator closed your post {self.post.heading}",
            "body": "",  # TODO: If we implement closed post feedback, include
                         # that here
            "post": self.post.id,
            "comment": None,
            "reply": None,
            "queue": None,
        }
