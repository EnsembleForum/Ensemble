from typing import TypedDict
from .identifiers import UserId


class IUserRegisterInfo(TypedDict):
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


class IUserBasicInfo(TypedDict):
    """
    Basic info about a user
    """
    name_first: str
    name_last: str
    username: str
    user_id: UserId


class IUserBasicInfoList(TypedDict):
    """
    List of basic info about users
    """
    users: list[IUserBasicInfo]


class IUserProfile(TypedDict):
    """
    Detailed info about a user
    """
    name_first: str
    name_last: str
    username: str
    email: str
    user_id: UserId
