from typing import TypedDict
from .identifiers import TagId


class ITagBasicInfo(TypedDict):
    tag_id: TagId
    name: str


class ITagId(TypedDict):
    tag_id: TagId


class ITagList(TypedDict):
    tags: list[ITagBasicInfo]
