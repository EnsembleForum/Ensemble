"""
# Ensemble request / Browse / Reply

Routes for browsing replies on the forum
"""
from typing import cast as __cast
from backend.types.identifiers import ReplyId, CommentId
from backend.types.react import IUserReacted
from backend.types.reply import IReplyId, IReplyFullInfo
from backend.types.auth import JWT
from ..consts import URL as __URL
from ..helpers import (
    post as __post,
    get as __get,
    put as __put,
    delete as __delete,
)

__URL = f"{__URL}/browse/reply"


def view(token: JWT, reply_id: ReplyId) -> IReplyFullInfo:
    """
    # GET `/browse/reply/view`

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

    ## Errors

    ### 400
    * Invalid reply ID

    ### 403
    * User does not have permission `PostView`
    """
    return __cast(
        IReplyFullInfo,
        __get(
            token,
            f"{__URL}/view",
            {
                "reply_id": reply_id,
            },
        ),
    )


def create(token: JWT, comment_id: CommentId, text: str) -> IReplyId:
    """
    # POST `/browse/reply/create`

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

    ## Errors

    ### 400
    * Invalid parent comment ID
    * Empty reply text

    ### 403
    * User does not have permission `PostComment`
    """
    return __cast(
        IReplyId,
        __post(
            token,
            f"{__URL}/create",
            {
                "comment_id": comment_id,
                "text": text,
            },
        ),
    )


def edit(
    token: JWT,
    reply_id: ReplyId,
    text: str,
):
    """
    # PUT `/browse/reply/edit`

    Edits the text of the comment

    ## Permissions
    * `PostCreate`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Body
    * `reply_id` (`int`): identifier of the comment
    * `text` (`str`): new text of the reply
                        (should be given the old text if unedited)

    ## Errors

    ### 400
    * Invalid reply ID
    * Empty reply text
    * Editing a deleted reply

    ### 403
    * User does not have permission `PostCreate`
    * User attempting to edit another user's reply
    """
    __put(
        token,
        f"{__URL}/edit",
        {
            "reply_id": reply_id,
            "text": text,
        },
    )


def delete(token: JWT, reply_id: ReplyId):
    """
    # DELETE `/browse/reply/delete`

    Deletes a reply.

    ## Permissions
    * `DeletePosts`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Params
    * `reply_id` (`int`): identifier of the reply

    ## Errors

    ### 400
    * Invalid reply ID

    ### 403
    * User does not have permission `DeletePosts` when they aren't the reply
      author
    """
    __delete(
        token,
        f"{__URL}/delete",
        {
            "reply_id": reply_id,
        },
    )


def react(token: JWT, reply_id: ReplyId) -> IUserReacted:
    """
    # PUT `/browse/reply/react`

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

    ## Errors

    ### 400
    * Invalid reply ID

    ### 403
    * User does not have permission `PostView`
    """
    return __cast(
        IUserReacted,
        __put(
            token,
            f"{__URL}/react",
            {
                "reply_id": reply_id,
            },
        )
    )
