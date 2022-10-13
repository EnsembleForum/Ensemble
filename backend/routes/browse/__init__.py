"""
# Backend / Routes / Browse

Browse routes
"""
import json
from flask import Blueprint, request
from backend.models.post import Post
from backend.models.queue import Queue
from backend.models.user import User
from backend.types.queue import IQueueFullInfoList, IQueueId
from backend.types.post import IPostBasicInfoList, IPostId
from .post_view import post_view
from .queue_view import queue_view
from .comment_view import comment_view
from .reply_view import reply_view
from backend.util.tokens import uses_token

browse = Blueprint("browse", "browse")
browse.register_blueprint(post_view, url_prefix="/post_view")
browse.register_blueprint(queue_view, url_prefix="/queue_view")
browse.register_blueprint(comment_view, url_prefix="/comment_view")
browse.register_blueprint(reply_view, url_prefix="/reply_view")


@browse.get("/post_list")
@uses_token
def post_list(*_) -> IPostBasicInfoList:
    """
    Get a list of posts

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostBasicInfoList`: List of basic info of posts
    """
    posts = Post.all()

    posts_info = [p.basic_info for p in posts]

    return {"posts": posts_info}


@browse.post("/create")
@uses_token
def create(user: User, *_) -> IPostId:
    """
    Create a post

    ## Body:
    * `token` (`JWT`): JWT of the user
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags attached to the new post (ignore for sprint 1)

    ## Returns:
    * `IPostId`: identifier of the post
    """
    data = json.loads(request.data)
    heading: str = data["heading"]
    text: str = data["text"]
    tags: list[int] = data["tags"]

    post_id = Post.create(user, heading, text, tags).id

    return {"post_id": post_id}

@browse.post("/queue_create")
@uses_token
def queue_create(user: User, *_) -> IQueueId:
    """
    Create a post

    ## Body:
    * `token` (`JWT`): JWT of the user
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags attached to the new post (ignore for sprint 1)

    ## Returns:
    * `IPostId`: identifier of the post
    """
    data = json.loads(request.data)
    queue_name: str = data["queue_name"]

    queue_id = Queue.create(queue_name).id

    return {"queue_id": queue_id}

__all__ = [
    "browse",
]
