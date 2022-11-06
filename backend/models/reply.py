"""
# Backend / Models / Reply
"""
from backend.types.reply import IReplyFullInfo
from .tables import TReply, TReplyReacts
from .user import User
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import ReplyId
from typing import cast, TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from .comment import Comment


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
        comment: 'Comment',
        text: str,
    ) -> "Reply":
        """
        Create a new reply

        ### Args:
        * `author` (`User`): user id of author

        * `comment_id` (`Comment`): comment the reply belongs to

        * `text` (`str`): contents of reply

        ### Returns:
        * `Reply`: the Reply object
        """
        assert_valid_str_field(text, "reply")

        val = (
            TReply(
                {
                    TReply.author: author.id,
                    TReply.text: text,
                    TReply.parent: comment.id,
                    # TReply.thanks: [],
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
    def parent(self) -> "Comment":
        """
        The comment this reply belongs to

        ### Returns:
        * `Comment`: comment
        """
        from .comment import Comment
        return Comment(self._get().parent)

    @property
    def thanks(self) -> int:
        """
        Returns the number of 'thanks' reacts

        ### Returns:
        * int: number of 'thanks' reacts
        """
        return cast(
            int,
            TReplyReacts.count()
            .where(TReplyReacts.reply == self.id).run_sync()
        )

    def has_reacted(self, user: User) -> bool:
        """
        Returns whether the user has reacted to this comment
        """
        return cast(
            bool,
            TReplyReacts.count()
            .where(TReplyReacts.reply == self.id,
                   TReplyReacts.user == user.id).run_sync()
        )

    def react(self, user: User):
        """
        React to the reply if the user has not reacted to the reply
        Unreact to the reply if the user has reacted to the reply

        ### Args:
        * `user` (`User`): User reacting/un-reacting to the reply
        """
        if not self.has_reacted(user):
            TReplyReacts(
                {
                    TReplyReacts.user: user.id,
                    TReplyReacts.reply: self.id,
                }
            ).save().run_sync()
        else:
            TReplyReacts.delete()\
                .where(TReplyReacts.user == user.id,
                       TReplyReacts.reply == self.id)\
                .run_sync()

    @property
    def timestamp(self) -> datetime:
        """
        Returns the timestamp of when the reply was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

    def full_info(self, user: User) -> IReplyFullInfo:
        """
        Returns the full info of a reply

        ### Returns:
        * IReplyFullInfo: Dictionary containing full info a reply
        """
        return {
            "reply_id": self.id,
            "author": self.author.id,
            "thanks": self.thanks,
            "text": self.text,
            "timestamp": int(self.timestamp.timestamp()),
            "user_reacted": self.has_reacted(user),
        }
