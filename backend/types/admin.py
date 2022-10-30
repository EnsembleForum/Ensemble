"""
# Backend / Types / Admin

Types for admin functions
"""
from typing import TypedDict, Literal, TypeGuard


class IIsFirstRun(TypedDict):
    """
    Return type for admin/is_first_run
    """
    value: bool


RequestType = Literal['get', 'post', 'put', 'delete']


def is_valid_request_type(t: str) -> TypeGuard[RequestType]:
    """
    Returns whether a string is a valid request type

    ### Args:
    * `val` (`str`): value to check

    ### Returns:
    * `TypeGuard[RequestType]`: whether it's valid
    """
    return t in ['get', 'post', 'put', 'delete']
