from typing import TypedDict
from .identifiers import CommentId, PostId, UserId


class IReacts(TypedDict):
    """
    Aggregate of reactions to a post/comment/reply

    * `thanks`: `int`
    * `me_too`: `int`
    """
    thanks: int
    me_too: int


class IPostBasicInfo(TypedDict):
    """
    Basic info about a post

    * `author`: `UserId`
    * `heading`: `str`
    * `post_id`: `PostId`
    * `tags`: `list[int]`
    * `me_too`: `int`
    * `private`: `bool`
    * `anonymous`: `bool`
    """
    author: UserId
    heading: str
    post_id: PostId
    tags: list[int]
    me_too: int
    private: bool
    anonymous: bool


class IPostBasicInfoList(TypedDict):
    """
    List of basic info about posts

    * `posts`: `list`, containing dictionaries of:
        * `author`: `UserId`
        * `heading`: `str`
        * `post_id`: `PostId`
        * `tags`: `list[int]`
        * `me_too`: `list[UserId]`
        * `private`: `bool`
        * `anonymous`: `bool`
    """
    posts: list[IPostBasicInfo]


class IPostId(TypedDict):
    """
    Identifier of a post

    * `post_id`: `PostId`
    """
    post_id: PostId


class IPostFullInfo(TypedDict):
    """
    Full info about a post

    * `author`: `UserId`
    * `heading`: `str`
    * `text`: `str`
    * `tags`: `list[int]`
    * `me_too`: `int`
    * `comments`: `list[CommentId]`
    * `timestamp`: `int`
    * `private`: `bool`
    * `anonymous`: `bool`
    * `author_reacted`: `bool`
    """
    author: UserId
    heading: str
    text: str
    tags: list[int]
    me_too: int
    author_reacted: bool
    comments: list[CommentId]
    timestamp: int
    private: bool
    anonymous: bool
