"""
# Backend / Models / Reply
"""
from .tables import TUser, TPost, TComment, TReply
from .user import User
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_text_valid
from backend.types.identifiers import CommentId, ReplyId
from backend.types.post import IReacts
from typing import cast
from datetime import datetime


class Reply:
    """
    Represents a reply of Ensemble
    """

    def __init__(self, id: ReplyId):
        """
        Create a comment object shadowing an existing in the database

        ### Args:
        * `id` (`int`): reply id

        ### Raises:
        * `KeyError`: reply does not exist
        """
        assert_id_exists(TReply, id, "Reply")
        self.__id = id

    @classmethod
    def create(
        cls,
        author: User,
        comment_id: CommentId,
        text: str,
    ) -> "Reply":
        """
        Create a new reply

        ### Args:
        * `author` (`int`): user id of author

        * `text` (`str`): contents of reply

        * `comment_id` (`CommentId`): CommentId of the comment the reply belongs to

        ### Returns:
        * `Reply`: the Reply object
        """
        assert_id_exists(TUser, author.id)
        assert_id_exists(TPost, comment_id, "Comment")
        assert_text_valid(text, "reply")

        val = (
            TComment(
                {
                    TComment.author: author.id,
                    TComment.text: text,
                    TComment.me_too: 0,
                    TComment.parent: comment_id,
                    TComment.thanks: 0,
                    TComment.timestamp: int(datetime.now().timestamp()),
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(ReplyId, val["id"])
        return Reply(id)

    @classmethod
    def delete(cls, reply_id: ReplyId) -> ReplyId:
        """
        Deletes a reply from the database

        ### Returns:
        * `ReplyId`: identifier of the deleted reply
        """
        TReply.delete().where(TReply.id == reply_id).run_sync()
        return reply_id

    def _get(self) -> TReply:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TReply, self.__id)

    @property
    def id(self) -> ReplyId:
        """
        Identifier of the reply
        """
        return self.__id

    @property
    def text(self) -> str:
        """
        The text of the reply
        """
        return self._get().text

    @text.setter
    def text(self, new_text: str):
        assert_text_valid(new_text, "reply")
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

    @me_too.setter
    def me_too(self, new_me_too: int):
        row = self._get()
        row.me_too = new_me_too
        row.save().run_sync()

    @property
    def thanks(self) -> int:
        """
        Returns the number of 'thanks' reacts

        ### Returns:
        * int: number of 'thanks' reacts
        """
        return self._get().thanks

    @thanks.setter
    def thanks(self, new_thanks: int):
        row = self._get()
        row.thanks = new_thanks
        row.save().run_sync()

    @property
    def timestamp(self) -> int:
        """
        Returns the timestamp of when the reply was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp: int):
        row = self._get()
        row.timestamp = new_timestamp
        row.save().run_sync()

    def update_timestamp(self):
        self.timestamp = int(datetime.now().timestamp())

    @property
    def reacts(self) -> IReacts:
        """
        Returns the reactions to the reply

        ### Returns:
        * IReacts: Dictionary containing the reactions
        """
        return {
            "thanks": self.thanks,
            "me_too": self.me_too,
        }
