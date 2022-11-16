"""
# Request / tags

Helper functions for requesting tags routes
"""
from typing import cast
from backend.types.identifiers import PostId, TagId
from backend.types.tag import ITagBasicInfo, ITagId
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, delete


URL = f"{URL}/tags"


def get_tag(token: JWT, tag_id: TagId) -> ITagBasicInfo:
    """
    ## GET `/tags/get_tag`

    Get the info of a tag

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Returns
    Object containing:
        * `tag_id` (`int`): ID of the tag
        * `name` (`str`): name of the tag
    """
    return cast(
        ITagBasicInfo,
        get(
            token,
            f"{URL}/get_tag",
            {"tag_id": tag_id, }
        )
    )


def create_tag(token: JWT, tag_name: str) -> ITagBasicInfo:
    """
    ## PUT `/tags/new_tag`

    Create a new tag

    ## Permissions
    * `ManageTags`

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `tag_name` (`str`): name of the new tag
    """

    return cast(
        ITagBasicInfo,
        post(
            token,
            f"{URL}/new_tag",
            {"tag_name": tag_name, }
        )
    )


def delete_tag(token: JWT, tag_id: TagId):
    """
    ## DELETE `/tags/delete_tag`

    Delete a tag

    ## Permissions
    * `ManageTags`

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `tag_id` (`int`): identifier of the new tag
    """
    delete(
        token,
        f"{URL}/delete_tag",
        {"tag_id": tag_id, }
    )


def add_tag_to_post(token: JWT, post_id: PostId, tag_id: TagId) -> ITagId:
    """
    ## POST `/tags/post_add_tag`

    Adds a tag to a post

    ## Permissions
    * `PostView`

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `tag_id` (`int`): identifier of the tag to be added
    * `post_id` (`int`): identifier of the post
    """
    return cast(
        ITagId,
        post(
            token,
            f"{URL}/post_add_tag",
            {
                "post_id": post_id,
                "tag_id": tag_id,
            }
        )
    )


def remove_tag_from_post(token: JWT, post_id: PostId, tag_id: TagId):
    """
    ## DELETE `/tags/post_remove_tag`

    Removes a tag from a post

    ## Permissions
    * `PostView`

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `tag_id` (`int`): identifier of the tag to be removed
    * `post_id` (`int`): identifier of the post
    """
    delete(
        token,
        f"{URL}/post_remove_tag",
        {
            "post_id": post_id,
            "tag_id": tag_id,
        }
    )
