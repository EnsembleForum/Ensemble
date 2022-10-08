"""
# Tests / Integration / Request / Admin
"""
from backend.types.admin import IIsFirstRun
from typing import cast
from ..consts import URL
from ..helpers import get

URL = f"{URL}/admin"


def is_first_run() -> IIsFirstRun:
    """
    Returns whether the datastore is empty

    ## Returns:
    * { value: bool }
    """
    return cast(IIsFirstRun, get(f"{URL}/is_first_run", {}))
