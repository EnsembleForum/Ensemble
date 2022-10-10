"""
# Backend / Util / Tokens

Code used for cleanly unwrapping JWT tokens from routes
"""
from flask import request
from functools import wraps
from typing import cast, Callable, TypeVar, ParamSpec, Concatenate
from backend.models.token import Token
from backend.types.auth import JWT
from backend.types.identifiers import UserId
from backend.util import http_errors

T = TypeVar('T')
P = ParamSpec('P')


def uses_token(
    func: Callable[Concatenate[UserId, JWT, P], T]
) -> Callable[P, T]:
    """
    Decorate a route function, declaring that it requires a token.

    This modifies its parameters, so that it must accept a user_id as well as
    the original token.

    ### Usage:

    If you need to access the user_id or token data:

    ```py
    @app.post('/my_route)
    @uses_token
    def my_route(user_id: UserId, token: JWT) -> dict:
        ...
        return {}
    ```

    Or if you don't:

    ```py
    @app.post('/my_other_route)
    @uses_token
    def my_other_route(*_) -> dict:
        ...
        return {}
    ```

    ### Args:
    * `func` (`Callable[Concatenate[UserId, JWT, P], T]`): route callback
      function.

    ### Returns:
    * `Callable[P, T]`: decorated callback function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            token: JWT = cast(JWT, request.headers["token"])
        except KeyError:
            raise http_errors.Unauthorized(
                "This route expected an authentication token, but couldn't "
                "find it in the request header"
            )
        user_id = Token.fromJWT(token).user.id
        return func(user_id, token, *args, **kwargs)

    return wrapper
