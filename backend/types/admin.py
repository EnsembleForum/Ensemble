"""
# Backend / Types / Admin

Types for admin functions
"""
from typing import TypedDict


class IIsFirstRun(TypedDict):
    """
    Return type for admin/is_first_run
    """
    value: bool
