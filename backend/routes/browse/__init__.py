"""
# Backend / Routes / Browse

Browse routes
"""
import json
from flask import Blueprint, request
from backend.models.post import Post
from backend.models.user import User
from backend.models.tag import Tag
from backend.models.exam_mode import ExamMode
from backend.models.permissions import Permission
from backend.types.post import IPostBasicInfoList, IPostId
from backend.types.identifiers import TagId
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
    search_term: str = request.args["search_term"]
    if len(search_term) > 0:
        posts_info = [p.basic_info(user)
                      for p in Post.search_posts(user, search_term)]
    else:
        posts_info = [p.basic_info(user) for p in Post.can_view_list(user)]

    return {"posts": posts_info}


@browse.post("/create")
@uses_token
def create(user: User, *_) -> IPostId:
    user.permissions.assert_can(Permission.PostCreate)

    data = json.loads(request.data)
    heading: str = data["heading"]
    text: str = data["text"]
    tags: list[TagId] = data["tags"]
    tags_list: list[Tag] = [Tag(i) for i in tags]
    private: bool = data["private"]
    anonymous: bool = data["anonymous"]

    if ExamMode.is_enabled() and not private:
        user.permissions.assert_can(Permission.PostOverrideExam)

    post_id = Post.create(user, heading, text, tags_list, private, anonymous).id
    return {"post_id": post_id}


__all__ = [
    "browse",
]
