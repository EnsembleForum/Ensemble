from typing import TypedDict


class IUserReacted(TypedDict):
    """
    Whether the user has reacted to a post/comment/reply

    * `user_reacted`: `bool`
    """

    user_reacted: bool
