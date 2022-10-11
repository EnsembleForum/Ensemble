"""
# Backend / Models / Comment
"""
from backend.types.comment import ICommentFullInfo
from .tables import TReply, TUser, TPost, TComment
from .user import User
from .reply import Reply
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import PostId, CommentId
from backend.types.post import IReacts
from typing import cast
from datetime import datetime


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
        post_id: PostId,
        text: str,
    ) -> "Comment":
        """
        Create a new comment

        ### Args:
        * `author` (`int`): user id of author

        * `text` (`str`): contents of comment

        * `post_id` (`PostId`): PostId of the post the comment belongs to

        ### Returns:
        * `Comment`: the comment object
        """
        assert_id_exists(TUser, author.id)
        assert_id_exists(TPost, post_id, "Post")
        assert_valid_str_field(text, "comment")

        val = (
            TComment(
                {
                    TComment.author: author.id,
                    TComment.text: text,
                    TComment.me_too: 0,
                    TComment.parent: post_id,
                    TComment.thanks: 0,
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
    def me_too(self) -> int:
        """
        Returns the number of 'me too' reacts

        ### Returns:
        * int: number of 'me too' reacts
        """
        return self._get().me_too

    def increment_me_too(self):
        row = self._get()
        row.me_too += 1
        row.save().run_sync()

    def decrement_me_too(self):
        row = self._get()
        row.me_too -= 1
        row.save().run_sync()

    @property
    def thanks(self) -> int:
        """
        Returns the number of 'thanks' reacts

        ### Returns:
        * int: number of 'thanks' reacts
        """
        return self._get().thanks

    def increment_thanks(self):
        row = self._get()
        row.thanks += 1
        row.save().run_sync()

    def decrement_thanks(self):
        row = self._get()
        row.thanks -= 1
        row.save().run_sync()

    @property
    def timestamp(self) -> datetime:
        """
        Returns the timestamp of when the comment was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

    @property
    def reacts(self) -> IReacts:
        """
        Returns the reactions to the comment

        ### Returns:
        * IReacts: Dictionary containing the reactions
        """
        return {
            "thanks": self.thanks,
            "me_too": self.me_too,
        }

    @property
    def full_info(self) -> ICommentFullInfo:
        """
        Returns the full info of a comment

        ### Returns:
        * ICommentFullInfo: Dictionary containing full info a comment
        """
        return {
            "author": self.author.id,
            "reacts": self.reacts,
            "text": self.text,
            "replies": [r.id for r in self.replies],
            "timestamp": int(self.timestamp.timestamp()),
        }
