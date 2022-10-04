from typing import TypedDict
from .identifiers import UserId


class IUserBasicDetails(TypedDict):
    """
    Basic user details used when registering a new user
    """
    name_first: str
    name_last: str
    username: str
    email: str


class IUserIdList(TypedDict):
    """
    List of user IDs for newly generated users
    """
    user_ids: list[UserId]
