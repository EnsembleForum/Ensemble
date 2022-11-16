"""
Contains the blueprints for routes that are used for testing and debugging.

These routes should be disabled in the production environment, perhaps using
and environment variable to enabled/disabled them?
"""
import sys
import json
from colorama import Fore
from flask import Blueprint, request
from backend.models import User, Token, Permission
from backend.util import http_errors, db_status, setup
from backend.util.debug import debug_active
from backend.types.debug import IEcho, IEnabled
from backend.types.auth import IAuthInfo
from backend.types.errors import IErrorInfo
from typing import NoReturn

__debug = Blueprint('debug', 'debug')


@__debug.get('/enabled')
def enabled() -> IEnabled:
    return {"value": True}


@__debug.get('/echo')
def echo() -> IEcho:
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


@__debug.delete('/clear')
def clear() -> dict:
    db_status.clear_all()
    return {}


@__debug.post('/shutdown')
def shutdown() -> dict:
    print("Initiated server shutdown")
    # TODO
    return {}


@__debug.get('/fail')
def fail() -> NoReturn:
    raise Exception("You brought this upon yourself.")


# Unsafe init to improve testing performance
@__debug.post('/unsafe_init')
def unsafe_init() -> IAuthInfo:
    data = json.loads(request.data.decode('utf-8'))
    address: str = data["address"]
    request_type = str(data["request_type"]).lower()
    username_param: str = data["username_param"]
    password_param: str = data["password_param"]
    success_regex: str = data["success_regex"]
    username: str = data["username"]
    password: str = data["password"]
    email: str = data["email"]
    name_first: str = data["name_first"]
    name_last: str = data["name_last"]
    return setup.init(
        address,
        request_type,
        username_param,
        password_param,
        success_regex,
        username,
        password,
        email,
        name_first,
        name_last,
        # Skip slow checks
        skip_slow_checks=True,
    )


# Unsafe init to improve testing performance
@__debug.post('/unsafe_login')
def unsafe_login() -> IAuthInfo:
    data = json.loads(request.data.decode('utf-8'))
    username = data["username"]
    try:
        u = User.from_username(username)
    except http_errors.BadRequest:
        raise http_errors.BadRequest("Username not registered") from None
    return {
        "user_id": u.id,
        "token": Token.create(u).encode(),
        "permissions": [
            {
                "permission_id": p.value,
                "value": u.permissions.can(p),
            } for p in Permission
        ],
    }


# Dummy debug containing no routes
__dummy_debug = Blueprint('dummy_debug', 'debug')


@__dummy_debug.get('/enabled')
def not_enabled() -> IEnabled:
    return {"value": False}


@__dummy_debug.route('/<path:path>')
def debug_not_found(path) -> tuple[IErrorInfo, int]:
    return {
        "code": 404,
        "heading": "Not found",
        "description": "Debug routes are disabled in a production environment",
        "traceback": None,
    }, 404


# Only export the debug routes if debugging
if debug_active():
    debug = __debug
else:
    debug = __dummy_debug
