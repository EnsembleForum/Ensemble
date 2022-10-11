"""
# Backend / Models / Reply
"""
from backend.types.reply import IReplyFullInfo
from .tables import TComment, TReply
from .user import User
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
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
        * `IdNotFound`: reply does not exist
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

        * `comment_id` (`CommentId`): comment the reply belongs to

        ### Returns:
        * `Reply`: the Reply object
        """
        assert_id_exists(TComment, comment_id, "Comment")
        assert_valid_str_field(text, "reply")

        val = (
            TReply(
                {
                    TReply.author: author.id,
                    TReply.text: text,
                    TReply.me_too: 0,
                    TReply.parent: comment_id,
                    TReply.thanks: 0,
                    TReply.timestamp: datetime.now()
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
        assert_valid_str_field(new_text, "reply")
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

    def me_too_inc(self):
        row = self._get()
        row.me_too += 1
        row.save().run_sync()

    def me_too_dec(self):
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

    def thanks_inc(self):
        row = self._get()
        row.thanks += 1
        row.save().run_sync()

    def thanks_dec(self):
        row = self._get()
        row.thanks -= 1
        row.save().run_sync()

    @property
    def timestamp(self) -> datetime:
        """
        Returns the timestamp of when the reply was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

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

    @property
    def full_info(self) -> IReplyFullInfo:
        """
        Returns the full info of a reply

        ### Returns:
        * IReplyFullInfo: Dictionary containing full info a reply
        """
        return {
            "author": self.author.id,
            "reacts": self.reacts,
            "text": self.text,
            "timestamp": int(self.timestamp.timestamp()),
        }
