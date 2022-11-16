"""
# Backend / Routes / Browse

Browse routes
"""
import json
from flask import Blueprint, request
from backend.models.post import Post
from backend.models.user import User
from backend.models.exam_mode import ExamMode
from backend.models.permissions import Permission
from backend.types.post import IPostBasicInfoList, IPostId
from .post import post
from .comment import comment
from .reply import reply
from backend.util.tokens import uses_token

browse = Blueprint("browse", "browse")
browse.register_blueprint(post, url_prefix="/post_view")
browse.register_blueprint(comment, url_prefix="/comment_view")
browse.register_blueprint(reply, url_prefix="/reply_view")


__all__ = [
    "browse",
]
