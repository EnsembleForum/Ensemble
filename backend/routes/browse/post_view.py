"""
# Backend / Routes / Browse / Post View

Post View routes
"""
import json
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.models.post import Post
from backend.models.user import User
from backend.models.comment import Comment
from backend.types.identifiers import PostId
from backend.types.post import IPostFullInfo
from backend.types.comment import ICommentId
from backend.util import http_errors
from backend.util.tokens import uses_token

post_view = Blueprint("post_view", "post_view")


@post_view.get("")
@uses_token
def get_post(user: User, *_) -> IPostFullInfo:
    user.permissions.assert_can(Permission.PostView)
    post_id = PostId(request.args["post_id"])
    post = Post(post_id)
    return post.full_info


@post_view.put("/edit")
@uses_token
def edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.PostCreate)
    data = json.loads(request.data)
    post_id: PostId = data["post_id"]
    new_heading: str = data["heading"]
    new_text: str = data["text"]
    new_tags: list[int] = data["tags"]

    post = Post(post_id)

    if user != post.author:
        raise http_errors.Forbidden("Attempting to edit another user's post")

    post.heading = new_heading
    post.text = new_text
    post.tags = new_tags
    return {}


@post_view.delete("/self_delete")
@uses_token
def delete(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.PostCreate)
    post = Post(PostId(request.args["post_id"]))

    if user != post.author:
        raise http_errors.Forbidden("Attempting to delete another user's post")

    post.delete()
    return {}


@post_view.post("/comment")
@uses_token
def comment(user: User, *_) -> ICommentId:
    user.permissions.assert_can(Permission.PostComment)
    data = json.loads(request.data)
    text: str = data["text"]
    post = Post(data["post_id"])

    comment_id = Comment.create(user, post, text).id

    return {"comment_id": comment_id}


@post_view.put("/react")
@uses_token
def react(user: User, *_) -> dict:
    """
    Add or remove a 'Me Too' react by the user to a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post to react to
    * `token` (`JWT`): JWT of the user
    """
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    post = Post(data["post_id"])
    post.react(user)

    return {}
