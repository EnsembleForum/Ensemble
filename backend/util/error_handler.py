"""
# Backend / Util / Error handler
"""
import traceback
from .http_errors import HTTPException
from backend.types.errors import IErrorInfo
from .debug import debug_active
from typing import Callable, TypeVar, ParamSpec
from functools import wraps


T = TypeVar("T", bound=Exception)
P = ParamSpec("P")


def decorate_error_handlers(
    func: Callable[[T], IErrorInfo]
) -> Callable[[T], tuple[IErrorInfo, int]]:
    """
    Decorator to make error handling nicer
    """
    @wraps(func)
    def wrapper(err: T) -> tuple[IErrorInfo, int]:
        ret = func(err)
        return ret, ret["code"]

    return wrapper


@decorate_error_handlers
def http_error_handler(err: HTTPException) -> IErrorInfo:
    """
    Default error handler for HTTP errors

    Returns error info as JSON

    ### Args:
    * `err` (`HTTPException`): error to handle
    """
    # Only include traceback if we're debugging
    if debug_active():
        trace = "\n".join(traceback.format_exception(err))
    else:
        trace = None
    # Type checks - all exceptions should have this
    if err.code is None:
        raise Exception(
            f"Error code not specified for exception {err}"
            f"{trace if trace is not None else ''}"
        )
    if err.description is None:
        raise Exception(
            f"Error description not specified for exception {err}"
            f"{trace if trace is not None else ''}"
        )
    # Finally return the info
    return {
        "code": err.code,
        "heading": type(err).__name__,
        "description": err.description,
        "traceback": trace,
    }


@decorate_error_handlers
def general_error_handler(err: Exception) -> IErrorInfo:
    """
    Error handler for other exceptions

    Gives an error 500

    ### Args:
    * `err` (`Exception`): _description_

    ### Returns:
    * `IErrorInfo`: _description_
    """
    # Only include traceback if we're debugging
    if debug_active():
        trace = "\n".join(traceback.format_exception(err))
    else:
        trace = None
    # Finally return the info
    return {
        "code": 500,
        "heading": "Internal server error",
        "description": str(err),
        "traceback": trace,
    }
