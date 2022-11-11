from typing import TypedDict, Optional
from .identifiers import CommentId, PostId, UserId


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
    * `answered`: `Optional[CommentId]`
    * `queue`: `str`
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
    answered: Optional[CommentId]
    queue: str


# {
#     'total_posts': int,
#     'total_comments': int,
#     'total_replies': int,
#     'top_posters': [{'user_id':int, 'num_posts':int}],       # top 10 posters
#     'top_commenters': [{'user_id':int, 'num_comments':int}], # top 10
#     'top_repliers': [{'user_id':int, 'num_replies':int}],    # top 10
# }


# {
#     'total_posts': int,
#     'total_comments': int,
#     'total_replies': int,
#     'students': {
#         'top_posters': [{'user_id':int, 'num_posts':int}],
#         'top_commenters': [{'user_id':int, 'num_comments':int}],
#         'top_repliers': [{'user_id':int, 'num_replies':int}],
#     },
#     'staff': {
#         'top_posters': [{'user_id':int, 'num_posts':int}],
#         'top_commenters': [{'user_id':int, 'num_comments':int}],
#         'top_repliers': [{'user_id':int, 'num_replies':int}],
#     },
#     'all': {
#         'top_posters': [{'user_id':int, 'num_posts':int}],
#         'top_commenters': [{'user_id':int, 'num_comments':int}],
#         'top_repliers': [{'user_id':int, 'num_replies':int}],
#     }
# }
