from typing import TypedDict
from .identifiers import TagId


class ITagBasicInfo(TypedDict):
    """
    Basic info of a tag

    * `tag_id`: `TagId`
    * `name`: `str`
    """
    tag_id: TagId
    name: str


class ITagId(TypedDict):
    """
    Identifier of a tag

    * `tag_id`: `TagId`
    """
    tag_id: TagId


class ITagList(TypedDict):
    """
    List of basic info about tags

    * `tags`: `list`, containing dictionaries of:
        * `tag_id`: `TagId`
        * `name`: `str`
    """
    tags: list[ITagBasicInfo]
