"""
# Request / Browse

Helper functions for requesting post browsing code
"""
from typing import cast
from backend.types.comment import (
    ICommentFullInfo,
    ICommentId,
    ICommentAccepted
)
from backend.types.reply import IReplyId
from backend.types.identifiers import CommentId, PostId, ReplyId, TagId
from backend.types.post import (
    IPostBasicInfoList,
    IPostFullInfo,
    IPostId,
    IPostClosed,
    IPostReported
)
from backend.types.react import IUserReacted
from backend.types.tag import ITagBasicInfo, ITagId
from backend.types.reply import IReplyFullInfo
from backend.types.auth import JWT
from .consts import URL
from .helpers import post, get, put, delete


URL = f"{URL}/browse"


def post_list(token: JWT, search_term: str = "") -> IPostBasicInfoList:
    """
    ## GET `/browse/post_list`

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
            * `reported`: (`bool`): whether this post is reported
    """
    return cast(
        IPostBasicInfoList,
        get(
            token,
            f"{URL}/post_list",
            {
                "search_term": search_term,
            }
        ),
    )


def post_view(token: JWT, post_id: PostId) -> IPostFullInfo:
    """
    # GET `/browse/post_view`

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
    * `reported`: (`bool`): whether this post is reported
    """
    return cast(
        IPostFullInfo,
        get(
            token,
            f"{URL}/post_view",
            {
                "post_id": post_id,
            },
        ),
    )


def post_create(
    token: JWT, heading: str, text: str, tags: list[int],
    private: bool = False, anonymous: bool = False
) -> IPostId:
    """
    ## POST `/browse/create`

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
    return cast(
        IPostId,
        post(
            token,
            f"{URL}/create",
            {
                "heading": heading,
                "text": text,
                "tags": tags,
                "private": private,
                "anonymous": anonymous,
            },
        ),
    )


def post_edit(
    token: JWT,
    post_id: PostId,
    heading: str,
    text: str,
    tags: list[int],
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
    put(
        token,
        f"{URL}/post_view/edit",
        {
            "post_id": post_id,
            "heading": heading,
            "text": text,
            "tags": tags,
        },
    )


def post_delete(token: JWT, post_id: PostId):
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
    delete(
        token,
        f"{URL}/post_view/delete",
        {"post_id": post_id, }
    )


def comment_delete(token: JWT, comment_id: CommentId):
    """
    # DELETE `/browse/comment_view/delete`

    Deletes a comment.

    ## Permissions
    * `DeletePosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `comment_id` (`int`): identifier of the comment
    """
    delete(
        token,
        f"{URL}/comment_view/delete",
        {"comment_id": comment_id, }
    )


def reply_delete(token: JWT, reply_id: ReplyId):
    """
    # DELETE `/browse/reply_view/delete`

    Deletes a reply.

    ## Permissions
    * `DeletePosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `reply_id` (`int`): identifier of the reply
    """
    delete(
        token,
        f"{URL}/reply_view/delete",
        {"reply_id": reply_id, }
    )


def add_comment(token: JWT, post_id: PostId, text: str) -> ICommentId:
    """
    # POST `/browse/post_view/comment`

    Creates a new comment on a post

    ## Permissions
    * `PostComment`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post to comment on
    * `text` (`str`): text of the comment

    ## Returns
    Object containing:
    * `comment_id` (`int`): identifier of the comment
    """
    return cast(
        ICommentId,
        post(
            token,
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

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `comment_id` (`int`): identifier of the comment

    ## Returns
    Object containing:
    * `author` (`int`): ID of the comment author
    * `thanks` (`int`): amount of thanks the comment received
    * `replies` (`list[int]`): list of reply IDs for replies to this comment
    * `text` (`str`): text of the comment
    * `timestamp` (`int`): UNIX timestamp of the comment
    * `user_reacted` (`bool`): True if the user has reacted to this reply
    * `accepted` (`bool`): True if the comment is marked as an answer,
                           False otherwise
    """
    return cast(
        ICommentFullInfo,
        get(
            token,
            f"{URL}/comment_view",
            {
                "comment_id": comment_id,
            },
        ),
    )


def add_reply(token: JWT, comment_id: CommentId, text: str) -> IReplyId:
    """
    # POST `/browse/comment_view/reply`

    Creates a new reply to a comment

    ## Permissions
    * `PostComment`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `comment_id` (`int`): identifier of the comment to reply to
    * `text` (`str`): text of the comment

    ## Returns
    Object containing:
    * `reply_id` (`int`): identifier of the reply
    """
    return cast(
        IReplyId,
        post(
            token,
            f"{URL}/comment_view/reply",
            {
                "comment_id": comment_id,
                "text": text,
            },
        ),
    )


def get_reply(token: JWT, reply_id: ReplyId) -> IReplyFullInfo:
    """
    # GET `/browse/reply_view`

    Get the detailed info of a reply

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `reply_id` (`int`): identifier of the reply

    ## Returns
    * `author` (`int`): ID of the author of the reply
    * `thanks`(`int`): amount of thanks the reply received
    * `text` (`str`): text of the reply
    * `timestamp` (`int`): UNIX timestamp of the reply
    * `user_reacted` (`bool`): True if the user has reacted to this reply
    """
    return cast(
        IReplyFullInfo,
        get(
            token,
            f"{URL}/reply_view",
            {
                "reply_id": reply_id,
            },
        ),
    )


def post_react(token: JWT, post_id: PostId) -> IUserReacted:
    """
    # PUT `/browse/post_view/react`

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
    return cast(
        IUserReacted,
        put(
            token,
            f"{URL}/post_view/react",
            {"post_id": post_id, }
        )
    )


def comment_react(token: JWT, comment_id: CommentId) -> IUserReacted:
    """
    # PUT `/browse/comment_view/react`

    Reacts to a comment if user has not reacted to that comment
    Un-reacts to a comment if the user has reacted to that comment

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `comment_id` (`int`): identifier of the comment

    ## Returns
    * `user_reacted` (`bool`): Whether the user reacted to the comment
    """
    return cast(
        IUserReacted,
        put(
            token,
            f"{URL}/comment_view/react",
            {"comment_id": comment_id, }
        )
    )


def reply_react(token: JWT, reply_id: ReplyId) -> IUserReacted:
    """
    # PUT `/browse/reply_view/react`

    Reacts to a reply if user has not reacted to that reply
    Un-reacts to a reply if the user has reacted to that reply

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `reply_id` (`int`): identifier of the reply

    ## Returns
    * `user_reacted` (`bool`): Whether the user reacted to the reply
    """
    return cast(
        IUserReacted,
        put(
            token,
            f"{URL}/reply_view/react",
            {"reply_id": reply_id, }
        )
    )

####


def get_tag(token: JWT, tag_id: TagId) -> ITagBasicInfo:
    return cast(
        ITagBasicInfo,
        get(
            token,
            f"{URL}/tags_view",
            {"tag_id": tag_id, }
        )
    )


def create_tag(token: JWT, tag_name: str) -> ITagBasicInfo:

    return cast(
        ITagBasicInfo,
        post(
            token,
            f"{URL}/tags_view/new_tag",
            {"tag_name": tag_name, }
        )
    )


def delete_tag(token: JWT, tag_id: TagId):
    delete(
        token,
        f"{URL}/tags_view/new_tag",
        {"tag_id": tag_id, }
    )


def add_tag_to_post(token: JWT, post_id: PostId, tag_id: TagId) -> ITagId:

    return cast(
        ITagId,
        post(
            token,
            f"{URL}/tags_view/add_tag_to_post",
            {
                "post_id": post_id,
                "tag_id": tag_id,
            }
        )
    )


def remove_tag_from_post(token: JWT, post_id: PostId, tag_id: TagId):
    delete(
        token,
        f"{URL}/tags_view/remove_tag_from_post",
        {
            "post_id": post_id,
            "tag_id": tag_id,
        }
    )


def accept_comment(token: JWT, comment_id: CommentId) -> ICommentAccepted:
    """
    # PUT `/browse/comment_view/accept`

    Toggles whether a comment is marked as accepted

    ## Permissions
    * `PostView`
    """
    return cast(
        ICommentAccepted,
        put(
            token,
            f"{URL}/comment_view/accept",
            {"comment_id": comment_id, }
        )
    )


def comment_edit(
    token: JWT,
    comment_id: CommentId,
    text: str,
):
    """
    # PUT `/browse/comment_view/edit`

    Edits the text of the comment

    ## Permissions
    * `PostCreate`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `comment_id` (`int`): identifier of the comment
    * `text` (`str`): new text of the comment
                        (should be given the old text if unedited)
    """
    put(
        token,
        f"{URL}/comment_view/edit",
        {
            "comment_id": comment_id,
            "text": text,
        },
    )


def reply_edit(
    token: JWT,
    reply_id: ReplyId,
    text: str,
):
    """
    # PUT `/browse/reply_view/edit`

    Edits the text of the comment

    ## Permissions
    * `PostCreate`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `reply_id` (`int`): identifier of the comment
    * `text` (`str`): new text of the reply
                        (should be given the old text if unedited)
    """
    put(
        token,
        f"{URL}/reply_view/edit",
        {
            "reply_id": reply_id,
            "text": text,
        },
    )


def close_post(
    token: JWT,
    post_id: PostId,
) -> IPostClosed:
    """
    # PUT `/browse/post_view/close`

    Close or un-close a post

    ## Permissions
    * `ClosePosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post
    """
    return cast(
        IPostClosed,
        put(
            token,
            f"{URL}/post_view/close",
            {
                "post_id": post_id,
            },
        )
    )


def report_post(
    token: JWT,
    post_id: PostId,
) -> IPostReported:
    """
    # PUT `/browse/post_view/report`

    Report a post

    ## Permissions
    * `ReportPosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Returns
    * `reported` (`bool`): Whether the post is marked as reported
    """
    return cast(
        IPostReported,
        put(
            token,
            f"{URL}/post_view/report",
            {
                "post_id": post_id,
            },
        )
    )


def unreport_post(
    token: JWT,
    post_id: PostId,
) -> IPostReported:
    """
    # PUT `/browse/post_view/unreport`

    Un-report a post

    ## Permissions
    * `ViewReports`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post

    ## Returns
    * `reported` (`bool`): Whether the post is marked as reported
    """
    return cast(
        IPostReported,
        put(
            token,
            f"{URL}/post_view/unreport",
            {
                "post_id": post_id,
            },
        )
    )
