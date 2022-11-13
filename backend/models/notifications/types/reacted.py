"""
# Backend / Models / Notifications / Types / Reacted

Notification for "Someone reacted to your post/comment/reply"
"""
from backend.models.post import Post
from .. import NotificationType
from .. import Notification
from ...user import User
from ...comment import Comment
from ...reply import Reply
from backend.types.notifications import INotificationInfo


class NotificationReacted(Notification):
    """
    Notification for "Someone reacted to your post/comment/reply"
    """

    @classmethod
    def create(
        cls,
        user_to: User,
        ref: Post | Comment | Reply,
    ) -> 'NotificationReacted':
        """
        Create a notification that someone reacted to your post/comment/reply

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

        return NotificationReacted(cls._create(
            user_to,
            NotificationType.Reacted,
            post=post,
            comment=comment,
            reply=reply,
        ))

    def _get_info(self) -> INotificationInfo:
        if self._reply is not None:
            action = "Your reply received thanks"
            title = self._reply.text
            reply_id = self._reply.id
            comment_id = self._reply.parent.id
            post_id = self._reply.parent.parent.id
        elif self._comment is not None:
            action = "Your comment received thanks"
            title = self._comment.text
            reply_id = None
            comment_id = self._comment.id
            post_id = self._comment.parent.id
        else:
            assert self._post is not None
            action = "Your post received a me too"
            title = self._post.heading
            reply_id = None
            comment_id = None
            post_id = self._post.id
        return {
            "notification_id": self.id,
            "user_from": None,
            "seen": self.seen,
            "heading": action,
            "body": title,
            "post": post_id,
            "comment": comment_id,
            "reply": reply_id,
            "queue": None,
        }
