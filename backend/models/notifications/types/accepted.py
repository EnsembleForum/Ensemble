"""
# Backend / Models / Notifications / Types / Accepted

Notification for "Someone accepted your answer for [post]"
"""
from backend.models.post import Post
from .. import NotificationType
from .. import Notification
from ...user import User
from ...comment import Comment
from backend.types.notifications import INotificationInfo


class NotificationAccepted(Notification):
    """
    Notification for "[user] accepted your answer for [post]"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        user_from: User,
        comment: Comment,
    ) -> 'NotificationAccepted':
        """
        Create a notification that someone accepted your answer

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `user_from` (`User`): user who accepted the answer

        * `ref` (`Comment`): reference to the comment that was accepted

        ### Returns:
        * `NotificationCommented`: notification object
        """
        post = comment.parent
        comment = comment

        return NotificationAccepted(cls._create(
            user_to,
            NotificationType.Accepted,
            user_from,
            post,
            comment,
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
    def comment(self) -> Comment:
        c = self._comment
        assert c is not None
        return c

    def _get_info(self) -> INotificationInfo:
        # If they wrote the comment
        if self.comment.author == self.user_to:
            head = "Answer accepted"
        # If they wrote the original post
        else:
            head = "Answer accepted on your post"
        return {
            "notification_id": self.id,
            "timestamp": self.timestamp,
            "seen": self.seen,
            "user_from": self.user_from.id,
            "heading": head,
            "body": self.comment.text,
            "post": self.post.id,
            "comment": self.comment.id,
            "reply": None,
            "queue": None,
        }
