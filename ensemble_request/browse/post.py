"""
# Ensemble request / Browse / Post

Routes for browsing posts on the forum
"""
import builtins
from typing import cast as __cast
from backend.types.identifiers import PostId
from backend.types.post import (
    IPostBasicInfoList,
    IPostFullInfo,
    IPostId,
    IPostClosed,
)
from backend.types.react import IUserReacted
from backend.types.auth import JWT
from ..consts import URL as __URL
from ..helpers import (
    post as __post,
    get as __get,
    put as __put,
    delete as __delete,
)

__URL = f"{__URL}/browse/post"


def list(token: JWT, search_term: str = "") -> IPostBasicInfoList:
    """
    ## GET `/browse/post/list`

    Get a list of posts visible to the give user

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `search_term` (`str`): search term used for searching
                             should be empty string if not searching

    ## Returns
    Object containing:
    * `posts`: List of objects, each containing
            * `post_id` (`int`): ID of the post
            * `author` (`Optional[int]`): ID of the creator of the post, or
              None if post is anonymous
            * `heading` (`str`): title of the post
            * `tags` (`list[int]`): list of tag IDs for the post (not
              implemented yet)
            * `me_too` (`int`): number of me too's, the post received
            * `private` (`bool`): whether this is a private post
            * `anonymous` (`bool`): whether this is an anonymous post
            * `answered`: (`bool`): whether this post is answered
            * `closed`: (`bool`): whether this post is closed
            * `deleted`: (`bool`): whether this post is deleted
            * `reported`: (`bool`): whether this post is reported. This is
              always false if the user performing the request doesn't have
              permission to view reported posts.
    """
    return __cast(
        IPostBasicInfoList,
        __get(
            token,
            f"{__URL}/list",
            {
                "search_term": search_term,
            }
        ),
    )


def view(token: JWT, post_id: PostId) -> IPostFullInfo:
    """
    # GET `/browse/post/view`

    Get the detailed info of a post.

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `post_id` (`int`): identifier of the post

    ## Returns
    Object containing
    * `author` (`Optional[int]`): ID of the creator of the post, or None if
      post is anonymous
    * `heading` (`str`): heading of the post
    * `text` (`str`): main text of the post
    * `tags` (`list[int]`): list of tag IDs for the post
    * `me_too` (`int`): number of me too's, the post received
    * `comments` (`list[int]`): list of IDs of comments
    * `timestamp` (`int`): UNIX timestamp of the post
    * `private` (`bool`): whether this is a private post
    * `anonymous` (`bool`): whether this is an anonymous post
    * `user_reacted` (`bool`): whether the user has reacted to this post
    * `answered` (`Optional[int]`): CommentId of the accepted comment,
                                    None if no comment is accepted
    * `closed`: (`bool`): whether this post is closed
    * `queue` (`QueueId`): queue that this post belongs to
    * `deleted`: (`bool`): whether this post is deleted
    * `reported`: (`bool`): whether this post is reported. This is always false
      if the user performing the request doesn't have permission to view
      reported posts.
    """
    return __cast(
        IPostFullInfo,
        __get(
            token,
            f"{__URL}/view",
            {
                "post_id": post_id,
            },
        ),
    )


def create(
    token: JWT,
    heading: str,
    text: str,
    tags: builtins.list[int],
    private: bool = False,
    anonymous: bool = False,
) -> IPostId:
    """
    ## POST `/browse/post/create`

    Create a new post on the forum

    ## Permissions
    * `PostCreate`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags attached to the new post (ignore for sprint 1)
    * `private` (`bool`): whether the post is private
    * `anonymous` (`bool`): whether the author is anonymous

    ## Returns
    Object containing:
    * `post_id` (`int`): identifier of the post
    """
    return __cast(
        IPostId,
        __post(
            token,
            f"{__URL}/create",
            {
                "heading": heading,
                "text": text,
                "tags": tags,
                "private": private,
                "anonymous": anonymous,
            },
        ),
    )


def edit(
    token: JWT,
    post_id: PostId,
    heading: str,
    text: str,
    tags: builtins.list[int],
):
    """
    # PUT `/browse/post_view/edit`

    Edits the heading/text/tags of the post

    ## Permissions
    * `PostCreate`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post
    * `heading` (`str`): new heading of the post
                        (should be given the old heading if unedited)
    * `text` (`str`): new text of the post
                        (should be given the old text if unedited)
    * `tags` (`list[int]`): new tags of the post (ignore for sprint 1)
    """
    __put(
        token,
        f"{__URL}/edit",
        {
            "post_id": post_id,
            "heading": heading,
            "text": text,
            "tags": tags,
        },
    )


def delete(token: JWT, post_id: PostId):
    """
    # DELETE `/browse/post_view/delete`

    Deletes a post.

    ## Permissions
    * `DeletePosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `post_id` (`int`): identifier of the post
    """
    __delete(
        token,
        f"{__URL}/delete",
        {"post_id": post_id, }
    )


def react(token: JWT, post_id: PostId) -> IUserReacted:
    """
    # PUT `/browse/post/react`

    Reacts to a post if user has not reacted to that post
    Un-reacts to a post if the user has reacted to that post

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Returns
    * `user_reacted` (`bool`): Whether the user reacted to the post
    """
    return __cast(
        IUserReacted,
        __put(
            token,
            f"{__URL}/react",
            {"post_id": post_id, }
        )
    )


def close(
    token: JWT,
    post_id: PostId,
) -> IPostClosed:
    """
    # PUT `/browse/post/close`

    Close or un-close a post

    ## Permissions
    * `ClosePosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post
    """
    return __cast(
        IPostClosed,
        __put(
            token,
            f"{__URL}/close",
            {
                "post_id": post_id,
            },
        )
    )


def report(
    token: JWT,
    post_id: PostId,
):
    """
    # PUT `/browse/post/report`

    Report a post

    ## Permissions
    * `ReportPosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post
    """
    __put(
        token,
        f"{__URL}/report",
        {
            "post_id": post_id,
        },
    )


def unreport(
    token: JWT,
    post_id: PostId,
):
    """
    # PUT `/browse/post/unreport`

    Un-report a post

    ## Permissions
    * `ViewReports`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post
    """
    __put(
        token,
        f"{__URL}/unreport",
        {
            "post_id": post_id,
        },
    )
