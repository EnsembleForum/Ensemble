"""
# Backend / Types / Auth

Types used within authentication
"""
from typing import NewType, TypedDict
from .identifiers import UserId


JWT = NewType('JWT', str)
"""Json Web Token type"""


class IAuthInfo(TypedDict):
    """
    Authentication info, returned when logging in

    * `user_id`: `UserId`
    * `token`: `JWT`
    """
    user_id: UserId
    token: JWT
