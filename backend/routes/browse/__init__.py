"""
# Backend / Routes / Browse

Browse routes
"""
from flask import Blueprint
from .post import post
from .comment import comment
from .reply import reply

browse = Blueprint("browse", "browse")
browse.register_blueprint(post, url_prefix="/post")
browse.register_blueprint(comment, url_prefix="/comment")
browse.register_blueprint(reply, url_prefix="/reply")


__all__ = [
    "browse",
]
