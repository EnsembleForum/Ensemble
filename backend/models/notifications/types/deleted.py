"""
# Backend / Models / Notifications / Types / Deleted

Notification for "A moderator deleted your post/comment/reply"
"""
from backend.models.post import Post
from .. import NotificationType
from .. import Notification
from ...user import User
from ...comment import Comment
from ...reply import Reply
from backend.types.notifications import INotificationInfo


class NotificationDeleted(Notification):
    """
    Notification for "A moderator deleted your post/comment/reply"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        ref: Post | Comment | Reply,
    ) -> 'NotificationDeleted':
        """
        Create a notification that a moderator deleted your post/comment/reply

        ### Args:
        * `user_to` (`User`): user receiving the notification

        * `ref` (`Post | Comment | Reply`): reference to the post/comment/reply

        ### Returns:
        * `NotificationDeleted`: notification object
        """
        if isinstance(ref, Post):
            post = ref
            comment = None
            reply = None
        elif isinstance(ref, Comment):
            post = ref.parent
            comment = ref
            reply = None
        else:
            post = ref.parent.parent
            comment = ref.parent
            reply = ref

        return NotificationDeleted(cls._create(
            user_to,
            NotificationType.Deleted,
            post=post,
            comment=comment,
            reply=reply,
        ))

    def _get_info(self) -> INotificationInfo:
        if self._reply is not None:
            type = "reply"
            title = self._reply.text
            reply_id = self._reply.id
            comment_id = self._reply.parent.id
            post_id = self._reply.parent.parent.id
        elif self._comment is not None:
            type = "comment"
            title = self._comment.text
            reply_id = None
            comment_id = self._comment.id
            post_id = self._comment.parent.id
        else:
            assert self._post is not None
            type = "post"
            title = self._post.heading
            reply_id = None
            comment_id = None
            post_id = self._post.id
        return {
            "notification_id": self.id,
            "timestamp": self.timestamp,
            "seen": self.seen,
            "user_from": None,
            "heading": f"Your {type} was deleted",
            "body": title,
            "post": post_id,
            "comment": comment_id,
            "reply": reply_id,
            "queue": None,
        }
