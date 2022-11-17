"""
# Ensemble request / Browse / Comment

Routes for browsing comments on the forum
"""
from typing import cast as __cast
from backend.types.identifiers import PostId, CommentId
from backend.types.react import IUserReacted
from backend.types.comment import (
    ICommentAccepted,
    ICommentId,
    ICommentFullInfo,
)
from backend.types.auth import JWT
from ..consts import URL as __URL
from ..helpers import (
    post as __post,
    get as __get,
    put as __put,
    delete as __delete,
)

__URL = f"{__URL}/browse/comment"


def view(token: JWT, comment_id: CommentId) -> ICommentFullInfo:
    """
    # GET `/browse/comment/view`

    Get the detailed info of a comment

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

    ## Errors

    ### 400
    * Invalid comment ID

    ### 403
    * User does not have permission `PostView`
    """
    return __cast(
        ICommentFullInfo,
        __get(
            token,
            f"{__URL}/view",
            {
                "comment_id": comment_id,
            },
        ),
    )


def create(token: JWT, post_id: PostId, text: str) -> ICommentId:
    """
    # POST `/browse/comment/create`

    Creates a new comment on a post

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `post_id` (`int`): identifier of the post to comment on
    * `text` (`str`): text of the comment

    ## Returns
    Object containing:
    * `comment_id` (`int`): identifier of the comment

    ## Errors

    ### 400
    * Empty comment contents
    * Invalid post ID

    ### 403
    * User does not have permission `PostComment`
    """
    return __cast(
        ICommentId,
        __post(
            token,
            f"{__URL}/create",
            {
                "text": text,
                "post_id": post_id,
            },
        ),
    )


def edit(
    token: JWT,
    comment_id: CommentId,
    text: str,
):
    """
    # PUT `/browse/comment/edit`

    Edits the text of the comment

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `comment_id` (`int`): identifier of the comment
    * `text` (`str`): new text of the comment
                        (should be given the old text if unedited)

    ## Errors

    ### 400
    * Invalid comment ID
    * Cannot edit a deleted comment
    * Empty text

    ### 403
    * User does not have permission `PostCreate`
    * User attempting to edit another user's comment
    """
    __put(
        token,
        f"{__URL}/edit",
        {
            "comment_id": comment_id,
            "text": text,
        },
    )


def delete(token: JWT, comment_id: CommentId):
    """
    # DELETE `/browse/comment/delete`

    Deletes a comment.

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `comment_id` (`int`): identifier of the comment

    ## Errors

    ### 400
    * Invalid comment ID

    ### 403
    * User does not have permission `DeletePosts` if they aren't the comment
      author
    """
    __delete(
        token,
        f"{__URL}/delete",
        {"comment_id": comment_id, }
    )


def react(token: JWT, comment_id: CommentId) -> IUserReacted:
    """
    # PUT `/browse/comment/react`

    Reacts to a comment if user has not reacted to that comment
    Un-reacts to a comment if the user has reacted to that comment

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `comment_id` (`int`): identifier of the comment

    ## Returns
    * `user_reacted` (`bool`): Whether the user reacted to the comment

    ## Errors

    ### 400
    * Invalid comment ID

    ### 403
    * User does not have permission `PostView`
    """
    return __cast(
        IUserReacted,
        __put(
            token,
            f"{__URL}/react",
            {"comment_id": comment_id, }
        )
    )


def accept(token: JWT, comment_id: CommentId) -> ICommentAccepted:
    """
    # PUT `/browse/comment/accept`

    Toggles whether a comment is marked as accepted

    ## Errors

    ### 400
    * Invalid comment ID

    ### 403
    * User does not have permission `PostView`
    * User is not author of post containing comment, or user does not have
      permission `CommentAccept`
    """
    return __cast(
        ICommentAccepted,
        __put(
            token,
            f"{__URL}/accept",
            {"comment_id": comment_id, }
        )
    )
