"""
# Backend / Routes / Browse / Reply View

Reply View routes
"""
import json
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.models.user import User
from backend.models.tag import Tag
from backend.types.identifiers import TagId
from backend.types.tag import ITagBasicInfo, ITagId, ITagList
from backend.util.tokens import uses_token

tags = Blueprint("tags", "tags")


@tags.get("get_tag")
@uses_token
def get_tag(user: User, *_) -> ITagBasicInfo:
    user.permissions.assert_can(Permission.PostView)
    tag_id = TagId(request.args["tag_id"])
    tag = Tag(tag_id)
    return tag.basic_info()


@tags.get("tags_list")
@uses_token
def get_tags_list(user: User, *_) -> ITagList:
    user.permissions.assert_can(Permission.PostView)
    return {"tags": list(map(lambda q: q.basic_info(), Tag.all()))}


@tags.post("/new_tag")
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


@tags.delete("/delete_tag")
@uses_token
def delete_tag(user: User, *_) -> dict:
    """
    Deleting the existence of a tag from a database

    ### Args:
    * `user` (`User`): user (who is an admin) deleting tags

    ### Returns:
    * `dict`: {}
    """
    user.permissions.assert_can(Permission.ManageTags)
    data = (request.args)
    tag_id = TagId(data["tag_id"])
    tag = Tag(tag_id)
    tag.delete()
    return {}