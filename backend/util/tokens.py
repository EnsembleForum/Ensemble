"""
# Backend / Util / Tokens

Code used for cleanly unwrapping JWT tokens from routes
"""
from flask import request
from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Concatenate
from backend.models.token import Token
from backend.models.user import User
from backend.types.auth import JWT
from backend.util import http_errors

T = TypeVar('T')
P = ParamSpec('P')


def uses_token(
    func: Callable[Concatenate[User, JWT, P], T]
) -> Callable[P, T]:
    """
    Decorate a route function, declaring that it requires a token.

    This modifies its parameters, so that it must accept a user as well as
    the original token.

    ### Usage:

    If you need to access the user or token data:

    ```py
    @app.post('/my_route)
    @uses_token
    def my_route(user: User, token: JWT) -> dict:
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
            bearer_token = request.headers["Authorization"]
            if not bearer_token.startswith("Bearer "):
                raise http_errors.Forbidden(
                    "Invalid format for JWT. Must be 'Bearer {token}'"
                )
            token: JWT = JWT(bearer_token.removeprefix('Bearer '))
        except KeyError:
            raise http_errors.Unauthorized(
                "This route expected an authentication token, but couldn't "
                "find it in the request header. Tokens must be given in the "
                "'Authorization' key"
            )
        user = Token.fromJWT(token).user
        return func(user, token, *args, **kwargs)

    return wrapper
