"""
# Backend / Util / Error handler
"""
import traceback
from werkzeug import exceptions as wz_exceptions
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
    return err.asJson()


@decorate_error_handlers
def werkzeug_error_handler(err: wz_exceptions.HTTPException) -> IErrorInfo:
    """
    Error handler for werkzeug exceptions

    ### Args:
    * `err` (`Exception`): error to handle

    ### Returns:
    * `IErrorInfo`: _description_
    """
    c = err.code if err.code is not None else 500
    return {
        "code": c,
        "heading": err.name,
        "description": err.description if err.description is not None else "",
        "traceback": None,
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
    trace = "\n".join(traceback.format_exception(err))
    traceback.print_exception(err)
    # Finally return the info
    return {
        "code": 500,
        "heading": "Internal server error",
        "description": str(err),
        "traceback": trace if debug_active() else None,
    }
