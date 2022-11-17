"""
# Request / tags

Helper functions for requesting tags routes
"""
from typing import cast
from backend.types.identifiers import TagId
from backend.types.tag import ITagBasicInfo, ITagList
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, delete


URL = f"{URL}/tags"


def get_tag(token: JWT, tag_id: TagId) -> ITagBasicInfo:
    """
    ## GET `/tags/get_tag`

    Get the info of a tag

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Params
    * `tag_id` (`int`): ID of tag to view

    ## Returns
    Object containing:
        * `tag_id` (`int`): ID of the tag
        * `name` (`str`): name of the tag

    ## Errors

    ### 400
    * Invalid tag ID

    ### 403
    * User does not have permission `PostView`
    """
    return cast(
        ITagBasicInfo,
        get(
            token,
            f"{URL}/get_tag",
            {"tag_id": tag_id, }
        )
    )


def tags_list(token: JWT) -> ITagList:
    """
    ## GET `/tags/tags_list`

    Get a list of all tags

    ## Header
    * `Authorization` (`JWT`): JWT of the user

    ## Returns
    Object containing:
    * `tags`: list of objects containing:
            * `tag_id` (`int`): ID of the tag
            * `name` (`str`): name of the tag

    ## Errors

    ### 403
    * User does not have permission `PostView`
    """
    return cast(
        ITagList,
        get(
            token,
            f"{URL}/tags_list",
            {}
        )
    )


def new_tag(token: JWT, tag_name: str) -> ITagBasicInfo:
    """
    ## POST `/tags/new_tag`

    Create a new tag

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Body
    * `tag_name` (`str`): name of the new tag

    ## Errors

    ### 400
    * Empty tag name
    * Tag with that name already exists

    ### 403
    * User does not have permission `ManageTags`
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

    ## Headers
    * `Authorization` (`JWT`): JWT of the user

    ## Params
    * `tag_id` (`int`): identifier of the new tag

    ## Errors

    ### 400
    * Invalid tag ID

    ### 403
    * User does not have permission `ManageTags`
    """
    delete(
        token,
        f"{URL}/delete_tag",
        {"tag_id": tag_id, }
    )
