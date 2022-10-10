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
    Get a list of posts

    ## Body:
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostBasicInfoList`: List of basic info of posts
    """
    return cast(
        IPostBasicInfoList,
        get(
            f"{URL}/post_list",
            {
                "token": token,
            },
        ),
    )


def post_create(
    token: JWT, heading: str, text: str, tags: list[int]
) -> IPostId:
    """
    Create a post

    ## Body:
    * `token` (`JWT`): JWT of the user
    * `heading` (`str`): heading of the post
    * `text` (`str`): text of the post
    * `tags` (`list[int]`): tags attached to the new post (ignore for sprint 1)

    ## Returns:
    * `IPostId`: identifier of the post
    """
    return cast(
        IPostId,
        post(
            f"{URL}/create",
            {
                "token": token,
                "heading": heading,
                "text": text,
                "tags": tags,
            },
        ),
    )


def post_view(token: JWT, post_id: PostId) -> IPostFullInfo:
    """
    Get the detailed info of a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostFullInfo`: Dictionary containing full info a post
    """
    return cast(
        IPostFullInfo,
        get(
            f"{URL}/post_view",
            {
                "token": token,
                "post_id": post_id,
            },
        ),
    )


def post_delete(token: JWT, post_id: PostId) -> IPostId:
    """
    Deletes a post

    ## Body:
    * `post_id` (`PostId`): identifier of the post
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IPostId`: identifier of the post
    """
    return cast(
        IPostId,
        put(
            f"{URL}/post_view/self_delete",
            {
                "token": token,
                "post_id": post_id,
            },
        ),
    )


def add_comment(token: JWT, post_id: PostId, text: str) -> ICommentId:
    """
    Creates a new comment

    ## Body:
    * `text` (`str`): text of the comment
    * `post_id` (`PostId`): identifier of the post to comment on
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `ICommentId`: identifier of the comment
    """
    return cast(
        ICommentId,
        post(
            f"{URL}/post_view/comment",
            {
                "token": token,
                "text": text,
                "post_id": post_id,
            },
        ),
    )


def get_comment(token: JWT, comment_id: CommentId) -> ICommentFullInfo:
    """
    Get the detailed info of a comment

    ## Body:
    * `comment_id` (`CommentId`): identifier of the comment
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `ICommentFullInfo`: Dictionary containing full info a comment
    """
    return cast(
        ICommentFullInfo,
        get(
            f"{URL}/comment_view",
            {
                "token": token,
                "comment_id": comment_id,
            },
        ),
    )


def add_reply(token: JWT, comment_id: CommentId, text: str) -> IReplyId:
    """
    Creates a new reply

    ## Body:
    * `text` (`str`): text of the comment
    * `comment_id` (`CommentId`): identifier of the comment to reply to
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IReplyId`: identifier of the reply
    """
    return cast(
        IReplyId,
        post(
            f"{URL}/comment_view/reply",
            {
                "token": token,
                "comment_id": comment_id,
                "text": text,
            },
        ),
    )


def get_reply(token: JWT, reply_id: ReplyId) -> IReplyFullInfo:
    """
    Get the detailed info of a reply

    ## Body:
    * `reply_id` (`ReplyId`): identifier of the reply
    * `token` (`JWT`): JWT of the user

    ## Returns:
    * `IReplyFullInfo`: Dictionary containing full info a reply
    """
    return cast(
        ICommentFullInfo,
        get(
            f"{URL}/reply_view",
            {
                "token": token,
                "reply_id": reply_id,
            },
        ),
    )
