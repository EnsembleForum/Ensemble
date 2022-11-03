from typing import TypedDict
from .identifiers import FeedbackId
from .post import IReacts


class IFeedbackId(TypedDict):
    """
    Identifier of a feedback

    * `feedback_id`: `FeedbackId`
    """

    feedback_id: FeedbackId


class IFeedbackFullInfo(TypedDict):
    """
    Full info about a comment

    * `title`: `str`
    * `message`: `str`
    """
    title: str
    message: str
