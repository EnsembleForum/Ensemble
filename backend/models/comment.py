"""
# Backend / Models / Comment
"""
from backend.types.comment import ICommentFullInfo
from .tables import TReply, TComment, TCommentReacts
from .user import User
from .reply import Reply
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import CommentId
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
                    # TComment.thanks: [],
                    TComment.timestamp: datetime.now()
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

    @classmethod
    def delete(cls, comment_id: CommentId) -> CommentId:
        """
        Deletes a comment from the database as well as all of its replies

        ### Returns:
        * `CommentId`: identifier of the deleted comment
        """
        TComment.delete().where(TComment.id == comment_id).run_sync()
        return comment_id

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
            "author": self.author.id,
            "thanks": self.thanks,
            "text": self.text,
            "replies": [r.id for r in self.replies],
            "timestamp": int(self.timestamp.timestamp()),
            "user_reacted": self.has_reacted(user),
        }
