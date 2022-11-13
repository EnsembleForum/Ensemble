"""
# Backend / Models / Notifications / Types / Commented

Notification for "Someone commented on your post, or replied to your comment"
"""
from backend.models.post import Post
from .. import NotificationType
from .. import Notification
from ...user import User
from ...comment import Comment
from ...reply import Reply
from backend.types.notifications import INotificationInfo


class NotificationCommented(Notification):
    """
    Notification for "Someone commented on your post, or replied to your
    comment"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        user_from: User,
        ref: Comment | Reply,
    ) -> 'NotificationCommented':
        """
        Create a notification that someone commented or replied to a user

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `user_from` (`User`): user who wrote the comment/reply

        * `ref` (`Comment | Reply`): reference to the comment/reply

        ### Returns:
        * `NotificationCommented`: notification object
        """
        if isinstance(ref, Comment):
            post = ref.parent
            comment = ref
            reply = None
        else:
            post = ref.parent.parent
            comment = ref.parent
            reply = ref

        return NotificationCommented(cls._create(
            user_to,
            NotificationType.Commented,
            user_from,
            post,
            comment,
            reply,
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
        if self._reply is not None:
            if self.comment.author == self.user_to:
                heading = "New reply to your comment"
            else:
                heading = "New reply on your post"
            body = self._reply.text
            reply_id = self._reply.id
        else:
            heading = "New comment on your post"
            body = self.comment.text
            reply_id = None
        return {
            "notification_id": self.id,
            "seen": self.seen,
            "user_from": self.user_from.id,
            "heading": heading,
            "body": body,
            "post": self.post.id,
            "comment": self.comment.id,
            "reply": reply_id,
            "queue": None,
        }
