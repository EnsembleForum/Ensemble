from typing import TypedDict, Optional
from .identifiers import UserId


class IUserRegisterInfo(TypedDict):
    """
    Basic user details used when registering a new user

    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `email`: `str`
    * `pronoun`: str`
    """
    name_first: str
    name_last: str
    username: str
    email: str
    pronoun: str


class IUserIdList(TypedDict):
    """
    List of user IDs for newly generated users

    * `user_ids`: list of
          * `int`
    """

    user_ids: list[UserId]


class IUserBasicInfo(TypedDict):
    """
    Basic info about a user

    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `user_id`: `int`
    """

    name_first: str
    name_last: str
    username: str
    user_id: UserId


class IUserBasicInfoList(TypedDict):
    """
    List of basic info about users

    * `users`: `list`, containing dictionaries of:
          * `name_first`: `str`
          * `name_last`: `str`
          * `username`: `str`
          * `user_id`: `int`
    """

    users: list[IUserBasicInfo]


class IUserProfile(TypedDict):
    """
    Detailed info about a user

    * `name_first`: `str`
    * `name_last`: `str`
    * `username`: `str`
    * `email`: `str`
    * `user_id`: `int`
    * `pronouns`: `Optional[str]`

    Note that this will eventually contain more properties such as pronouns and
    the like
    """

    name_first: str
    name_last: str
    username: str
    email: str
    pronouns: Optional[str]
    user_id: UserId
