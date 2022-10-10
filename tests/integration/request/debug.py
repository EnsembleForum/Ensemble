"""
# Tests / Integration / Functions / Debug

Functions that shadow server routes starting at /debug
"""
from typing import cast
from backend.types.debug import IEcho
from .consts import URL
from .helpers import get, delete, post


URL = f"{URL}/debug"


def echo(value: str) -> IEcho:
    """
    Echo an input. This returns the given value, but also prints it to stdout
    on the server. Useful for debugging tests.

    ## Params:
    * `value` (`str`): value to echo
    """
    return cast(IEcho, get(None, f"{URL}/echo", {"value": value}))


def clear() -> None:
    """
    Clear the database.
    """
    delete(None, f"{URL}/clear", {})


def shutdown() -> None:
    """
    Initiate a server shutdown.
    """
    post(None, f"{URL}/shutdown", {})
