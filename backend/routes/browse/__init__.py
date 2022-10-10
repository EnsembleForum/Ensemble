"""
# Backend / Routes / Browse

Browse routes
"""
import json
from flask import Blueprint, request
from backend.models.post import Post
from backend.models.token import Token
from backend.types.auth import JWT
from backend.types.identifiers import PostId, UserId
from backend.types.post import IPostBasicInfoList, IPostBasicInfo, IPostId
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
def post_list(*_) -> IPostBasicInfoList:
    """
    Get a list of posts

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostBasicInfoList`: List of basic info of posts
    """
    posts = Post.all()

    def basic_post_info(post: Post) -> IPostBasicInfo:
        return {
            "author": f"{post.author.name_first} {post.author.name_last}",
            "heading": post.heading,
            "post_id": post.id,
            "tags": post.tags,
            "reacts": post.reacts,
        }

    posts_info: list[IPostBasicInfo] = [basic_post_info(p) for p in posts]

    return {"posts": posts_info}


@browse.post("/create")
@uses_token
def create(user_id: UserId, token: JWT) -> IPostId:
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
    user_token: Token = Token.fromJWT(token)
    heading: str = data["heading"]
    text: str = data["text"]
    tags: list[int] = data["tags"]

    post_id: PostId = Post.create(user_token.user, heading, text, tags).id

    return {"post_id": post_id}


__all__ = [
    "browse",
]
