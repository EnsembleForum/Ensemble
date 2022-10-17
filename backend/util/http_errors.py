"""
# Backend / Util / HTTP Errors

Definitions for HTTP exceptions used by the server.

Note that these should only be raised directly if we want to ensure the error
is sent back to the user. Code in the `models` module should not raise these
directly, but instead should raise specific exceptions defined in
`backend.util.exceptions`.

## Usage

```py
from backend.util import http_errors

# In a request
if request_is_bad():
    raise http_errors.BadRequest("Some useful message")
```

## Attribution

Error code descriptions sourced from
[Mozilla's MDN docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status),
used under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/).
"""
from typing import Optional, TypeVar, Generic
from werkzeug.exceptions import HTTPException as _HTTPException
from werkzeug.wrappers import Response
from backend.types.errors import IErrorInfo


T = TypeVar("T", IErrorInfo, None)


class HTTPException(_HTTPException, Generic[T]):
    """
    Base HTTPException type in Ensemble
    """
    test_json: T

    def __init__(
        self,
        description: Optional[str] = None,
        response: Optional[Response] = None,
        test_json: T = None,
    ) -> None:
        self.test_json = test_json  # type: ignore
        super().__init__(description, response)


class BadRequest(HTTPException, Generic[T]):
    """
    The server cannot or will not process the request due to something that is
    perceived to be a client error (e.g., malformed request syntax, invalid
    request message framing, or deceptive request routing).
    """
    test_json: T
    code = 400


class Unauthorized(HTTPException, Generic[T]):
    """
    Although the HTTP standard specifies "unauthorized", semantically this
    response means "unauthenticated". That is, the client must authenticate
    itself to get the requested response.
    """
    test_json: T
    code = 401


class Forbidden(HTTPException, Generic[T]):
    """
    The client does not have access rights to the content; that is, it is
    unauthorized, so the server is refusing to give the requested resource.
    Unlike `Unauthorized`, the client's identity is known to the server.
    """
    test_json: T
    code = 403


class NotFound(HTTPException):
    """
    The server can not find the requested resource. In the browser, this means
    the URL is not recognized. In an API, this can also mean that the endpoint
    is valid but the resource itself does not exist. Servers may also send this
    response instead of `403 Forbidden` to hide the existence of a resource
    from an unauthorized client. This response code is probably the most well
    known due to its frequent occurrence on the web.
    """
    code = 404


class MethodNotAllowed(HTTPException):
    """
    The request method is known by the server but is not supported by the
    target resource. For example, an API may not allow calling DELETE to remove
    a resource.
    """
    code = 405


class InternalServerError(HTTPException, Generic[T]):
    """
    The server has encountered a situation it does not know how to handle.
    """
    test_json: T
    code = 500
