"""
# Backend / Models / Feedback
"""
from .tables import TFeedbackOptions
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import FeedbackId
from backend.types.feedback import IFeedbackId, IFeedbackFullInfo
from typing import cast


class Feedback:
    """
    Represents feedback in a post
    """
    def __init__(self, id: FeedbackId):
        """
        Create a post object shadowing an existing in the database

        ### Args:
        * `id` (`int`): post id

        ### Raises:
        * `IdNotFound`: post does not exist
        """
        assert_id_exists(TFeedbackOptions, id, "Feedback Option")
        self.__id = id

    def _get(self) -> TFeedbackOptions:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TFeedbackOptions, self.__id)

    @classmethod
    def create(
        cls,
        title,
        message,
    ) -> "Feedback":
        """
        Create a new feedback

        ### Args:
        * `title` (`int`): title of feedback

        * `message` (`str`): message

        ### Returns:
        * `Feedback`: the feedback object
        """
        assert_valid_str_field(title, "title")
        assert_valid_str_field(message, "message")

        val = (
            TFeedbackOptions(
                {
                    TFeedbackOptions.title: title,
                    TFeedbackOptions.message: message,
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(FeedbackId, val["id"])
        return Feedback(id)

    @classmethod
    def all(cls) -> list["Feedback"]:
        """
        Returns a list of all feedbacks
        in order of newest to oldest
        ### Returns:
        * `list[Feedback]`: list of feedbacks
        """
        return [
            Feedback(f["id"]) for f in
            TFeedbackOptions.select().order_by(TFeedbackOptions.id,
                                               ascending=False).run_sync()
        ]

    @property
    def id(self) -> FeedbackId:
        """
        Identifier of the post
        """
        return self.__id

    @property
    def title(self) -> str:
        """
        Returns title of feedback options
        """
        return self._get().title

    @title.setter
    def title(self, newTitle: str):
        assert_valid_str_field(newTitle, "new title")
        row = self._get()
        row.title = newTitle
        row.save().run_sync()

    @property
    def message(self) -> str:
        """
        Returns message of the post
        """
        return self._get().message

    @message.setter
    def message(self, newMessage: str):
        assert_valid_str_field(newMessage, "new message")
        row = self._get()
        row.title = newMessage
        row.save().run_sync()

    @property
    def full_info(self) -> IFeedbackFullInfo:
        """
        Returns the full info of a post

        ### Returns:
        * IPostFullInfo: Dictionary containing full info a post
        """
        return {
            "title": self.title,
            "message": self.message,
        }
