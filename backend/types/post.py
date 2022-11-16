from typing import TypedDict, Optional
from .identifiers import CommentId, PostId, UserId, TagId


class IPostBasicInfo(TypedDict):
    """
    Basic info about a post

    * `author`: `Optional[int]`
    * `heading`: `str`
    * `post_id`: `PostId`
    * `tags`: `list[int]`
    * `me_too`: `int`
    * `private`: `bool`
    * `anonymous`: `bool`
    * `closed`: `bool`
    * `deleted`: `bool`
    * `answered`: `bool`
    * `reported`: `bool`
    """
    post_id: PostId
    author: Optional[UserId]
    heading: str
    tags: list[int]
    me_too: int
    private: bool
    anonymous: bool
    answered: bool
    closed: bool
    deleted: bool
    reported: bool


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
        * `deleted`: `bool`
        * `answered`: `bool`
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

    * `author` (`Optional[int]`): author of post or None if anonymous
    * `heading` (`str`):
    * `text` (`str`):
    * `tags` (`list[int]`):
    * `me_too` (`int`):
    * `comments` (`list[CommentId]`):
    * `timestamp` (`int`):
    * `private` (`bool`):
    * `anonymous` (`bool`):
    * `closed` (`bool`):
    * `deleted` (`bool`):
    * `reported` (`bool`):
    * `user_reacted` (`bool`):
    * `answered` (`Optional[CommentId]`): ID of chosen answer if answered else
      none
    * `queue` (`str`):
    """
    post_id: PostId
    author: Optional[UserId]
    heading: str
    text: str
    tags: list[TagId]
    me_too: int
    user_reacted: bool
    comments: list[CommentId]
    timestamp: int
    private: bool
    anonymous: bool
    closed: bool
    deleted: bool
    reported: bool
    answered: Optional[CommentId]
    queue: str


class IPostClosed(TypedDict):
    """
    Whether a post is closed

    * `closed`: `bool`
    """
    closed: bool
