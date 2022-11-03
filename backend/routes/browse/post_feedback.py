import json
from flask import Blueprint, request
from backend.models.post import Post
from backend.models.feedback import Feedback
from backend.models.user import User
from backend.models.comment import Comment
from backend.types.identifiers import PostId, FeedbackId
from backend.types.post import IPostFullInfo, IPostId, IPostFeedback
from backend.types.feedback import IFeedbackId, IFeedbackFullInfo
from backend.types.comment import ICommentId
from backend.util import http_errors
from backend.util.tokens import uses_token

post_feedback = Blueprint("post_feedback", "post_feedback")


@post_feedback.get("")
@uses_token
def get_feedback(*_) -> IFeedbackFullInfo:
    """
    Get the detailed info of a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostFullInfo`: Dictionary containing full info a post
    """
    data = json.loads(request.data)
    feedback_id: FeedbackId = data["feedback_id"]
    feedback = Feedback(feedback_id)
    return feedback.full_info

@post_feedback.put("/edit")
@uses_token
def edit(*_) -> IFeedbackId:
    data = json.loads(request.data)
    feedback_id: FeedbackId = data["feedback_id"]
    feedback = Feedback(feedback_id)

    new_title = data["title"]
    new_message = data['message']
    feedback.title = new_title
    feedback.message = new_message

    return {"feedback_id": feedback_id}


@post_feedback.post("/add")
@uses_token
def add(*_) -> IFeedbackId:
    data = json.loads(request.data)
    title: str = data["title"]
    message = str(data["message"])

    feedback_id = Feedback.create(title, message).id

    return {"feedback_id": feedback_id}




'''
edit
add
mvvm
'''
