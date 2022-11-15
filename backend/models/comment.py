"""
# Backend / Models / Comment
"""
from backend.types.comment import ICommentFullInfo
from .tables import TReply, TComment, TCommentReacts
from .user import User
from .reply import Reply
from backend.models.permissions import Permission
from backend.models.queue import Queue
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import CommentId
from backend.util import http_errors
from typing import cast, TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from backend.models.post import Post


class Comment:
    """
    Represents a comment of Ensemble
    """

    def __init__(self, id: CommentId):
        """
        Create a comment object shadowing an existing in the database

        ### Args:
        * `id` (`int`): comment id

        ### Raises:
        * `IdNotFound`: comment does not exist
        """
        assert_id_exists(TComment, id, "Comment")
        self.__id = id

    @classmethod
    def create(
        cls,
        author: User,
        post: 'Post',
        text: str,
    ) -> "Comment":
        """
        Create a new comment

        ### Args:
        * `author` (`User`): creator of the comment

        * `post` (`Post`): post the comment belongs to

        * `text` (`str`): contents of comment

        ### Returns:
        * `Comment`: the comment object
        """
        assert_valid_str_field(text, "comment")

        val = (
            TComment(
                {
                    TComment.author: author.id,
                    TComment.text: text,
                    TComment.parent: post.id,
                    TComment.timestamp: datetime.now(),
                    TComment.deleted: False,
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(CommentId, val["id"])
        return Comment(id)

    @property
    def replies(self) -> list["Reply"]:
        """
        Returns a list of all replies belonging to the post
        in order of oldest to newest
        ### Returns:
        * `list[Reply]`: list of replies
        """
        return [
            Reply(r["id"])
            for r in TReply.select()
            .where(TReply.parent == self.__id)
            .order_by(TReply.id)
            .run_sync()
        ]

    @property
    def deleted(self) -> bool:
        """
        Whether the comment is deleted
        """
        return self._get().deleted

    @deleted.setter
    def deleted(self, new_status: bool):
        row = self._get()
        row.deleted = new_status
        row.save().run_sync()

    def delete(self):
        """
        Delete this comment
        """
        self.text = "[Deleted]"
        self.deleted = True

    def _get(self) -> TComment:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TComment, self.__id)

    @property
    def id(self) -> CommentId:
        """
        Identifier of the comment
        """
        return self.__id

    @property
    def text(self) -> str:
        """
        The text of the comment
        """
        return self._get().text

    @text.setter
    def text(self, new_text: str):
        assert_valid_str_field(new_text, "comment")
        row = self._get()
        row.text = new_text
        row.save().run_sync()

    @property
    def author(self) -> "User":
        """
        Returns a reference to the user that owns this token

        ### Returns:
        * `User`: user
        """
        return User(self._get().author)

    @property
    def parent(self) -> "Post":
        """
        The post this comment belongs to

        ### Returns:
        * `Post`: post
        """
        from .post import Post
        return Post(self._get().parent)

    @property
    def thanks(self) -> int:
        """
        Returns the number of 'thanks' reacts

        ### Returns:
        * int: number of 'thanks' reacts
        """
        return cast(
            int,
            TCommentReacts.count()
            .where(TCommentReacts.comment == self.id).run_sync()
        )

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Comment):
            return self.id == __o.id
        else:
            return False

    @property
    def accepted(self) -> bool:
        """
        Returns whether the comment has been marked as accepted
        """
        return self.parent.answered == self

    def accepted_toggle(self, user: User):
        """
        Mark comment as accepted if it was not
        Mark comment as unaccepted if it was accepted
        """
        if self.parent.author != user and\
                not user.permissions.can(Permission.CommentAccept):
            raise http_errors.Forbidden(
                "Do not have permissions mark as accepted"
            )

        if self.accepted:
            self.parent.answered = None
            self.parent.queue = Queue.get_main_queue()
        else:
            self.parent.answered = self
            self.parent.queue = Queue.get_answered_queue()

    def has_reacted(self, user: User) -> bool:
        """
        Returns whether the user has reacted to this comment
        """
        return cast(
            bool,
            TCommentReacts.count()
            .where(TCommentReacts.comment == self.id,
                   TCommentReacts.user == user.id).run_sync()
        )

    def react(self, user: User):
        """
        React to the comment if the user has not reacted to the comment
        Unreact to the comment if the user has reacted to the comment

        ### Args:
        * `user` (`User`): User reacting/un-reacting to the comment
        """
        if not self.has_reacted(user):
            TCommentReacts(
                {
                    TCommentReacts.user: user.id,
                    TCommentReacts.comment: self.id,
                }
            ).save().run_sync()
        else:
            TCommentReacts.delete()\
                .where(TCommentReacts.user == user.id,
                       TCommentReacts.comment == self.id)\
                .run_sync()

    @property
    def timestamp(self) -> datetime:
        """
        Returns the timestamp of when the comment was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

    def full_info(self, user: User) -> ICommentFullInfo:
        """
        Returns the full info of a comment

        ### Returns:
        * ICommentFullInfo: Dictionary containing full info a comment
        """
        return {
            "comment_id": self.id,
            "author": self.author.id,
            "thanks": self.thanks,
            "text": self.text,
            "replies": [r.id for r in self.replies],
            "timestamp": int(self.timestamp.timestamp()),
            "user_reacted": self.has_reacted(user),
            "accepted": self.accepted,
            "deleted": self.deleted,
        }
