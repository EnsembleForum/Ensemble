"""
# Backend / Types / Errors

Definitions for types associated with errors
"""
from typing import TypedDict, Optional


class IErrorInfo(TypedDict):
    """
    Contains information about an error

    * `code`: status code

    * `heading`: basic info on exception

    * `details`: detailed info on the exception

    * `traceback`: the exception traceback (only if we're in debug mode)
    """
    code: int
    heading: str
    description: str
    traceback: Optional[str]
