"""
Contains the blueprints for routes that are used for testing and debugging.

These routes should be disabled in the production environment, perhaps using
and environment variable to enabled/disabled them?
"""
import sys
from colorama import Fore
from flask import Blueprint, request
from backend.util import http_errors, db_status
from backend.util.debug import debug_active
from backend.types.debug import IEcho
from backend.types.errors import IErrorInfo
from typing import NoReturn

debug = Blueprint('debug', 'debug')


@debug.get('/echo')
def echo() -> IEcho:
    """
    Echo an input. This returns the given value, but also prints it to stdout
    on the server. Useful for debugging tests.

    ## Params:
    * `value` (`str`): value to echo
    """
    try:
        value = request.args['value']
    except KeyError:
        raise http_errors.BadRequest('echo route requires a `value` argument')

    to_print = f'{Fore.MAGENTA}[ECHO]\t\t{value}{Fore.RESET}'
    # Print it to both stdout and stderr to ensure it is seen across all logs
    # Otherwise it could be more difficult to figure out what's up with server
    # output
    print(to_print)
    print(to_print, file=sys.stderr)
    return {'value': value}


@debug.delete('/clear')
def clear() -> dict:
    """
    Clear the database.
    """
    db_status.clear_all()
    return {}


@debug.post('/shutdown')
def shutdown() -> dict:
    """
    Initiate a server shutdown.
    """
    print("Initiated server shutdown")
    # TODO
    return {}


@debug.get('/fail')
def fail() -> NoReturn:
    """
    Raise an error 500
    """
    raise Exception("You brought this upon yourself.")


# Dummy debug containing no routes
dummy_debug = Blueprint('dummy_debug', 'debug')


@dummy_debug.route('/<path:path>')
def debug_not_found(path) -> tuple[IErrorInfo, int]:
    return {
        "code": 404,
        "heading": "Not found",
        "description": "Debug routes are disabled in a production environment",
        "traceback": None,
    }, 404


# Only export the required routes
if debug_active():
    debug_export = debug
else:
    debug_export = dummy_debug
