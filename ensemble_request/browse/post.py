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

    ## Errors

    ### 403
    * User does not have permission `PostView`
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

    ## Errors

    ### 400
    * Invalid post ID

    ### 403
    * User does not have permission `PostView`
    * User does not have permission to view this post
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

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags IDs
    * `private` (`bool`): whether the post is private
    * `anonymous` (`bool`): whether the author is anonymous

    ## Returns
    Object containing:
    * `post_id` (`int`): identifier of the post

    ## Errors

    ### 400
    * Empty post heading
    * Empty post text
    * Invalid tag ID

    ### 403
    * User does not have permission `PostCreate`
    * User does not have permission `PostOverrideExam` when exam mode is active
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

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post
    * `heading` (`str`): new heading of the post
                        (should be given the old heading if unedited)
    * `text` (`str`): new text of the post
                        (should be given the old text if unedited)
    * `tags` (`list[int]`): list of new tag IDs for the post

    ## Errors

    ### 400
    * Invalid post ID
    * Invalid tag IDs
    * Empty new post heading
    * Empty new post text
    * Cannot edit a deleted post

    ### 403
    * User does not have permission `PostViewCreate`
    * User cannot edit another user's post
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

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `post_id` (`int`): identifier of the post

    ## Errors

    ### 400
    * Invalid post ID

    ### 403
    * User does not have permission `PostCreate`
    * User attempting to delete post they didn't author without `DeletePosts`
      permission
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

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Returns
    * `user_reacted` (`bool`): Whether the user reacted to the post

    ## Errors

    ### 400
    * Invalid post ID

    ### 403
    * User does not have permission `PostView`
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

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Errors

    ### 400
    * Invalid post ID

    ### 403
    * User does not have permission `ClosePosts`
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

    Toggle whether a post has been reported

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Errors

    ### 400
    * Invalid post ID

    ### 403
    * User does not have permission `ReportPosts`
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

    Remove all reports on a post. This action should be taken by moderators if
    they find that a report is invalid.

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Errors

    ### 400
    * Invalid post ID

    ### 403
    * User does not have permission `ViewReports`
    """
    __put(
        token,
        f"{__URL}/unreport",
        {
            "post_id": post_id,
        },
    )
