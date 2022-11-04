from typing import TypedDict
from .identifiers import CommentId, PostId, UserId, QueueId


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
    * `answered`: `bool`
    """
    post_id: PostId
    author: UserId
    heading: str
    tags: list[int]
    me_too: int
    private: bool
    anonymous: bool
    answered: bool


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
    * `user_reacted`: `bool`
    * `answered`: `bool`
    * `queue`: `QueueId`
    """
    post_id: PostId
    author: UserId
    heading: str
    text: str
    tags: list[int]
    me_too: int
    user_reacted: bool
    comments: list[CommentId]
    timestamp: int
    private: bool
    anonymous: bool
    answered: bool
    queue: QueueId
