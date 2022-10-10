"""
# Backend / Routes / Browse / Post View

Post View routes
"""
import json
from flask import Blueprint, request
from typing import cast
from backend.models.post import Post
from backend.models.token import Token
from backend.types.auth import JWT
from backend.models.comment import Comment
from backend.types.identifiers import PostId, CommentId
from backend.types.post import IPostFullInfo, IPostId
from backend.types.comment import ICommentId
from backend.util import http_errors

post_view = Blueprint("post_view", "post_view")


@post_view.get("")
def get_post() -> IPostFullInfo:
    """
    Get the detailed info of a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostFullInfo`: Dictionary containing full info a post
    """
    Token.fromJWT(cast(JWT, request.args["token"]))
    post_id: PostId = cast(PostId, request.args["post_id"])
    post = Post(post_id)
    return {
        "author": f"{post.author.name_first} {post.author.name_last}",
        "heading": post.heading,
        "text": post.text,
        "tags": post.tags,
        "reacts": post.reacts,
        "comments": [c.id for c in post.comments],
        "timestamp": post.timestamp,
    }


@post_view.put("/edit")
def edit() -> IPostId:
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
    token: Token = Token.fromJWT(data["token"])
    post_id: PostId = data["post_id"]
    new_heading: str = data["heading"]
    new_text: str = data["text"]
    new_tags: list[int] = data["tags"]

    post = Post(post_id)

    if token.user.id != post.author.id:
        raise http_errors.Forbidden("Attempting to edit another user's post")

    post.heading = new_heading
    post.text = new_text
    post.tags = new_tags
    return {"post_id": post.id}


@post_view.put("/self_delete")
def delete() -> IPostId:
    """
    Deletes a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostId`: identifier of the post
    """
    data = json.loads(request.data)
    post_id: PostId = data["post_id"]
    token: Token = Token.fromJWT(data["token"])

    post = Post(post_id)

    if token.user.id != post.author.id:
        raise http_errors.Forbidden("Attempting to delete another user's post")

    Post.delete(post_id)
    return {"post_id": post_id}


@post_view.post("/comment")
def comment() -> ICommentId:
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
    token: Token = Token.fromJWT(data["token"])
    text: str = data["text"]
    post_id: PostId = data["post_id"]

    comment_id: CommentId = Comment.create(token.user, post_id, text).id

    return {"comment_id": comment_id}
