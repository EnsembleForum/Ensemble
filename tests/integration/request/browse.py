"""
# Tests / Integration / Request / Browse

Helper functions for requesting auth code
"""
from typing import cast
from backend.types.post import IPostBasicInfoList, IPostId
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get


URL = f"{URL}/browse"


def post_list(token: JWT) -> IPostBasicInfoList:
    """
    Get a list of posts

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostBasicInfoList`: List of basic info of posts
    """
    return cast(
        IPostBasicInfoList,
        get(
            f"{URL}/post_list",
            {
                "token": token,
            },
        ),
    )


def post_create(token: JWT, heading: str, text: str, tags: list[int]) -> IPostId:
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
    return cast(
        IPostId,
        post(
            f"{URL}/create",
            {
                "token": token,
                "heading": heading,
                "text": text,
                "tags": tags,
            },
        ),
    )
