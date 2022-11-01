"""
# Backend / Routes / Browse

Browse routes
"""
import json
from flask import Blueprint, request
from backend.models.post import Post
from backend.models.user import User
from backend.models.permissions import Permission
from backend.types.post import IPostBasicInfoList, IPostId
from .post_view import post_view
from .comment_view import comment_view
from .reply_view import reply_view
from backend.util.tokens import uses_token

browse = Blueprint("browse", "browse")
browse.register_blueprint(post_view, url_prefix="/post_view")
browse.register_blueprint(comment_view, url_prefix="/comment_view")
browse.register_blueprint(reply_view, url_prefix="/reply_view")


@browse.get("/post_list")
@uses_token
def post_list(user: User, *_) -> IPostBasicInfoList:
    user.permissions.assert_can(Permission.PostView)

    posts_info = [p.basic_info for p in Post.can_view_list(user)]

    return {"posts": posts_info}


@browse.post("/create")
@uses_token
def create(user: User, *_) -> IPostId:
    user.permissions.assert_can(Permission.PostCreate)
    data = json.loads(request.data)
    heading: str = data["heading"]
    text: str = data["text"]
    tags: list[int] = data["tags"]
    private: bool = data["private"]

    post_id = Post.create(user, heading, text, tags, private).id

    return {"post_id": post_id}


__all__ = [
    "browse",
]
