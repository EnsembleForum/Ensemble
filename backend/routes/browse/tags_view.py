"""
# Backend / Routes / Browse / Reply View

Reply View routes
"""
import json
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.models.user import User
from backend.models.post import Post
from backend.models.tag import Tag
from backend.types.identifiers import TagId, PostId
from backend.types.tag import ITagBasicInfo, ITagId
from backend.util.tokens import uses_token

tags_view = Blueprint("tags_view", "tags_view")


@tags_view.get("")
@uses_token
def get_tag(*_) -> ITagBasicInfo:
    tag_id = TagId(request.args["tag_id"])
    tag = Tag(tag_id)
    return tag.basic_info()


@tags_view.post("/new_tag")
@uses_token
def create_tag(user: User, *_) -> ITagId:
    """
    Creating a new tag

    ### Args:
    * `new_tag_name` (`str`): new tag name

    ### Returns:
    * `ITagId`: ID of tag
    """
    user.permissions.assert_can(Permission.ManageTags)
    data = json.loads(request.data)
    tag_name = data["tag_name"]
    tag_id = Tag.create(tag_name).id

    return {"tag_id": tag_id}


@tags_view.delete("/delete_tag")
@uses_token
def delete_tag(user: User, *_) -> dict:
    """
    Deleting the existence of a tag from a databse

    ### Args:
    * `user` (`User`): user (who is an admin) deleting tags

    ### Returns:
    * `dict`: {}
    """
    user.permissions.assert_can(Permission.ManageTags)
    data = json.loads(request.data)
    tag_id = data["tag_id"]
    tag = Tag(tag_id)
    tag.delete()
    return {}


@tags_view.post("/add_tag_to_post")
@uses_token
def add_tag_to_post(*_) -> ITagId:
    """
    Adding a tag to a post

    ### Args:
    * `new_tag_id` (`TagId`): id of a tag already existing in TTags

    ### Returns:
    * `ITagId`: ID of tag
    """
    data = json.loads(request.data)
    post_id: PostId = data["post_id"]
    post = Post(post_id)
    tag_id = data["tag_id"]
    tag = Tag(tag_id)
    post.add_tag(tag)

    return {"tag_id": tag_id}


@tags_view.delete("/remove_tag_from_post")
@uses_token
def remove_tag_from_post(*_) -> dict:
    """
    Deleting a tag from a post

    ### Args:
    *

    ### Returns:
    * `dict`: {}
    """
    data = json.loads(request.data)
    post_id: PostId = data["post_id"]
    post = Post(post_id)
    tag_id = data["tag_id"]
    tag = Tag(tag_id)
    post.delete_tag(tag)

    return {}
