from typing import TypedDict
from .identifiers import CommentId, PostId


class IReacts(TypedDict):
    thanks: int
    me_too: int


class IPostBasicInfo(TypedDict):
    """
    Basic info about a post
    """

    author: str
    heading: str
    post_id: PostId
    tags: list[int]
    reacts: IReacts


class IPostBasicInfoList(TypedDict):
    """
    List of basic info about posts
    """

    posts: list[IPostBasicInfo]


class IPostId(TypedDict):
    """
    Identifier of a post
    """

    post_id: PostId


class IPostFullInfo(TypedDict):
    author: str
    heading: str
    text: str
    tags: list[int]
    reacts: IReacts
    comments: list[CommentId]
    timestamp: int
