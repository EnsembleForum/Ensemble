"""
# Request / Debug

Functions that shadow server routes starting at /debug
"""
from typing import cast, NoReturn
from backend.types.debug import IEcho
from .consts import URL
from .helpers import get, delete, post


URL = f"{URL}/debug"


def echo(value: str) -> IEcho:
    """
    ## GET `debug/echo`

    Echo an input. This returns the given value, but also prints it to stdout
    and stderr on the server. Useful for debugging tests.

    ## Params
    * `value` (`str`): value to echo

    ## Returns
    Object containing:
    * `value`: the same value
    """
    return cast(IEcho, get(None, f"{URL}/echo", {"value": value}))


def clear() -> None:
    """
    ## DELETE `debug/clear`

    Clear the database.
    """
    delete(None, f"{URL}/clear", {})


def shutdown() -> None:
    """
    ## POST `debug/shutdown`

    Initiate a server shutdown.

    Currently this route is unused.
    """
    post(None, f"{URL}/shutdown", {})


def fail() -> NoReturn:
    """
    ## GET `debug/fail`

    Raise a 500 error. Used to test error handling.
    """
    get(None, f"{URL}/fail", {})
    # If we reach this point then we have problems
    assert False
