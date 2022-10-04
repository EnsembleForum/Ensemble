"""
Contains the blueprints for routes that are used for testing and debugging.

These routes should be disabled in the production environment, perhaps using
and environment variable to enabled/disabled them?
"""
from colorama import Fore
from flask import Blueprint, request
from backend.util import http_errors
from backend.types.debug import IEcho

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

    print(f'{Fore.MAGENTA}[ECHO]\t\t{value}{Fore.RESET}')
    return {'value': value}


@debug.delete('/clear')
def clear() -> dict:
    """
    Clear the database.
    """
    # TODO
    return {}


@debug.post('/shutdown')
def shutdown() -> dict:
    """
    Initiate a server shutdown.
    """
    print("Initiated server shutdown")
    # TODO
    return {}
