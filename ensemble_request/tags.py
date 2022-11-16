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
    return cast(
        ITagBasicInfo,
        get(
            token,
            f"{URL}/get_tag",
            {"tag_id": tag_id, }
        )
    )


def create_tag(token: JWT, tag_name: str) -> ITagBasicInfo:

    return cast(
        ITagBasicInfo,
        post(
            token,
            f"{URL}/new_tag",
            {"tag_name": tag_name, }
        )
    )


def delete_tag(token: JWT, tag_id: TagId):
    delete(
        token,
        f"{URL}/delete_tag",
        {"tag_id": tag_id, }
    )


def add_tag_to_post(token: JWT, post_id: PostId, tag_id: TagId) -> ITagId:
    return cast(
        ITagId,
        post(
            token,
            f"{URL}/add_tag_to_post",
            {
                "post_id": post_id,
                "tag_id": tag_id,
            }
        )
    )


def remove_tag_from_post(token: JWT, post_id: PostId, tag_id: TagId):
    delete(
        token,
        f"{URL}/remove_tag_from_post",
        {
            "post_id": post_id,
            "tag_id": tag_id,
        }
    )
