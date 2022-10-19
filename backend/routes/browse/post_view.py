"""
# Backend / Routes / Browse / Post View

Post View routes
"""
import json
from flask import Blueprint, request
from typing import cast
from backend.models.post import Post
from backend.models.user import User
from backend.models.comment import Comment
from backend.types.identifiers import PostId, CommentId
from backend.types.post import IPostFullInfo, IPostId
from backend.types.comment import ICommentId
from backend.util import http_errors
from backend.util.tokens import uses_token

post_view = Blueprint("post_view", "post_view")


@post_view.get("")
@uses_token
def get_post(*_) -> IPostFullInfo:
    """
    Get the detailed info of a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostFullInfo`: Dictionary containing full info a post
    """
    post_id: PostId = cast(PostId, int(request.args["post_id"]))
    post = Post(post_id)
    return post.full_info


@post_view.put("/edit")
@uses_token
def edit(user: User, *_) -> IPostId:
    """
    Edits the heading/text/tags of the post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `heading` (`str`): new heading of the post
                        (should be given the old heading if unedited)
    * `text` (`str`): new text of the post
                        (should be given the old text if unedited)
    * `tags` (`list[int]`): new tags of the post (ignore for sprint 1)
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostId`: identifier of the post
    """
    data = json.loads(request.data)
    post_id: PostId = data["post_id"]
    new_heading: str = data["heading"]
    new_text: str = data["text"]
    new_tags: list[int] = data["tags"]

    post = Post(post_id)

    if user.id != post.author.id:
        raise http_errors.Forbidden("Attempting to edit another user's post")

    post.heading = new_heading
    post.text = new_text
    post.tags = new_tags
    return {"post_id": post.id}


@post_view.put("/self_delete")
@uses_token
def delete(user: User, *_) -> dict:
    """
    Deletes a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostId`: identifier of the post
    """
    data = json.loads(request.data)
    post_id = PostId(int(data["post_id"]))

    post = Post(post_id)

    if user.id != post.author.id:
        raise http_errors.Forbidden("Attempting to delete another user's post")

    Post.delete(post_id)
    return {}


@post_view.post("/comment")
@uses_token
def comment(user: User, *_) -> ICommentId:
    """
    Creates a new comment

    ## Body:
    * `text` (`str`): text of the comment
    * `post_id` (`PostId`): identifier of the post to comment on
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `ICommentId`: identifier of the comment
    """
    data = json.loads(request.data)
    text: str = data["text"]
    post = Post(data["post_id"])

    comment_id: CommentId = Comment.create(user, post, text).id

    return {"comment_id": comment_id}
