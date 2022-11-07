"""
# Backend / Models / Commented

Notification for "Someone commented on your post, or replied to your comment"
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
        Create a notification that someone commented or replied to a user

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `user_from` (`User`): user who wrote the comment/reply

        * `ref` (`Comment | Reply`): reference to the comment/reply

        ### Returns:
        * `NotificationCommented`: notification object
        """

        return NotificationClosed(cls._create(
            user_to,
            NotificationType.Closed,
            None,
            post,
            None,
            None,
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
        }
