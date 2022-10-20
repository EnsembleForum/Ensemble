"""
# Tests / Integration / Request / Browse

Helper functions for requesting auth code
"""
from typing import cast
from backend.types.comment import ICommentFullInfo, ICommentId
from backend.types.reply import IReplyId
from backend.types.identifiers import CommentId, PostId, ReplyId
from backend.types.post import IPostBasicInfoList, IPostFullInfo, IPostId
from backend.types.reply import IReplyFullInfo
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, put


URL = f"{URL}/browse"


def post_list(token: JWT) -> IPostBasicInfoList:
    """
    ## GET `/browse/post_list`

    Get a list of posts visible to the give user

    ## Header
    * `token` (`str`): JWT of the user

    ## Returns
    Object containing:
    * `posts`: List of objects, each containing
            * `post_id` (`int`): ID of the post
            * `author` (`int`): ID of the creator of the post
            * `heading` (`str`): title of the post
            * `tags` (`list[int]`): list of tag IDs for the post (not
              implemented yet)
            * `reacts`: object containing
                    * `thanks` (`int`): amount of thanks the post received
                    * `me_too` (`int`): number of me too's, the post received
    """
    return cast(
        IPostBasicInfoList,
        get(token,
            f"{URL}/post_list",
            {}
            ),
    )


def post_create(
    token: JWT, heading: str, text: str, tags: list[int]
) -> IPostId:
    """
    ## POST `/browse/create`

    Create a new post on the forum

    ## Header
    * `token` (`str`): JWT of the user

    ## Body
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags attached to the new post (ignore for sprint 1)

    ## Returns
    Object containing:
    * `post_id` (`int`): identifier of the post
    """
    return cast(
        IPostId,
        post(token,
             f"{URL}/create",
             {
                 "heading": heading,
                 "text": text,
                 "tags": tags,
             },
             ),
    )


def post_view(token: JWT, post_id: PostId) -> IPostFullInfo:
    """
    # GET `/browse/post_view`

    Get the detailed info of a post.

    ## Header
    * `token` (`str`): JWT of the user

    ## Params
    * `post_id` (`int`): identifier of the post

    ## Returns
    Object containing
    * `author` (`int`): ID of the post author
    * `heading` (`str`): heading of the post
    * `text` (`str`): main text of the post
    * `tags` (`list[int]`): list of tag IDs for the post
    * `reacts` (object containing):
            * `thanks` (`int`): amount of thanks the post received
            * `me_too` (`int`): number of me too's, the post received
    * `comments` (`list[int]`): list of IDs of comments
    * `timestamp` (`int`): UNIX timestamp of the post
    """
    return cast(
        IPostFullInfo,
        get(token,
            f"{URL}/post_view",
            {
                "post_id": post_id,
            },
            ),
    )


def post_edit(
    token: JWT,
    post_id: PostId,
    heading: str,
    text: str,
    tags: list[int],
) -> IPostId:
    """
    # PUT `/browse/post_view/edit`

    Edits the heading/text/tags of the post

    ## Header
    * `token` (`str`): JWT of the user

    ## Body
    * `post_id` (`PostId`): identifier of the post
    * `heading` (`str`): new heading of the post
                        (should be given the old heading if unedited)
    * `text` (`str`): new text of the post
                        (should be given the old text if unedited)
    * `tags` (`list[int]`): new tags of the post (ignore for sprint 1)

    ## Returns
    * `IPostId`: identifier of the post

    FIXME: Is it worthwhile returning the post ID given that they already know
    it?
    """
    return cast(
        IPostId,
        put(token,
            f"{URL}/post_view/edit",
            {
                "post_id": post_id,
                "heading": heading,
                "text": text,
                "tags": tags,
            },
            ),
    )


def post_delete(token: JWT, post_id: PostId) -> dict:
    """
    # DELETE `/browse/post_view/self_delete`

    Deletes a post. This route must be called by the owner of the post.

    ## Header
    * `token` (`str`): JWT of the user

    ## Params
    * `post_id` (`int`): identifier of the post

    ## Returns
    * `IPostId`: identifier of the post

    FIXME: Is it worthwhile returning the post ID given that they already know
    it?
    """
    return put(token,
               f"{URL}/post_view/self_delete",
               {"post_id": post_id, }
               )


def add_comment(token: JWT, post_id: PostId, text: str) -> ICommentId:
    """
    # POST `/browse/post_view/comment`

    Creates a new comment on a post

    ## Header
    * `token` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post to comment on
    * `text` (`str`): text of the comment

    ## Returns
    Object containing:
    * `comment_id` (`int`): identifier of the comment
    """
    return cast(
        ICommentId,
        post(token,
             f"{URL}/post_view/comment",
             {
                 "text": text,
                 "post_id": post_id,
             },
             ),
    )


def get_comment(token: JWT, comment_id: CommentId) -> ICommentFullInfo:
    """
    # GET `/browse/comment_view`

    Get the detailed info of a comment

    ## Header
    * `token` (`str`): JWT of the user

    ## Params
    * `comment_id` (`CommentId`): identifier of the comment

    ## Returns
    Object containing:
    * `author` (`int`): ID of the comment author
    * `reacts`: object containing
            * `thanks` (`int`): amount of thanks the comment received
            * `me_too` (`int`): number of me too's, the comment received
    * `replies` (`list[int]`): list of reply IDs for replies to this comment
    * `text` (`str`): text of the comment
    * `timestamp` (`int`): UNIX timestamp of the comment
    """
    return cast(
        ICommentFullInfo,
        get(token,
            f"{URL}/comment_view",
            {
                "comment_id": comment_id,
            },
            ),
    )


def add_reply(token: JWT, comment_id: CommentId, text: str) -> IReplyId:
    """
    # POST `/browse/comment_view/reply`

    Creates a new reply

    ## Header
    * `token` (`str`): JWT of the user

    ## Body
    * `comment_id` (`CommentId`): identifier of the comment to reply to
    * `text` (`str`): text of the comment

    ## Returns
    Object containing:
    * `reply_id` (`int`): identifier of the reply
    """
    return cast(
        IReplyId,
        post(token,
             f"{URL}/comment_view/reply",
             {
                 "comment_id": comment_id,
                 "text": text,
             },
             ),
    )


def get_reply(token: JWT, reply_id: ReplyId) -> IReplyFullInfo:
    """
    # POST `/browse/reply_view`

    Get the detailed info of a reply

    ## Header
    * `token` (`str`): JWT of the user

    ## Params
    * `reply_id` (`ReplyId`): identifier of the reply

    ## Returns
    * `author` (`int`): ID of the author of the reply
    * `reacts`: object containing
            * `thanks` (`int`): amount of thanks the reply received
            * `me_too` (`int`): number of me too's, the reply received
    * `text` (`str`): text of the reply
    * `timestamp` (`int`): UNIX timestamp of the reply
    """
    return cast(
        IReplyFullInfo,
        get(token,
            f"{URL}/reply_view",
            {
                "reply_id": reply_id,
            },
            ),
    )
