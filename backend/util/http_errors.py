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
import traceback
from typing import Optional
from backend.types.errors import IErrorInfo
from .debug import debug_active


class HTTPException(Exception):
    """
    Base HTTPException type in Ensemble
    """
    code: int
    heading: str
    description: str
    traceback: Optional[str]

    def __init__(
        self,
        code: int,
        description: str,
        traceback: Optional[str],
    ) -> None:
        """
        Create a basic HTTP exception

        ### Args:
        * `code` (`int`): status code

        * `description` (`str`): description of error

        * `traceback` (`Optional[str]`): traceback of error, used in testing
          API (not in backend)
        """
        self.code = code
        self.heading = codes[code][0]
        self.description = description
        self.traceback = traceback

    def __repr__(self) -> str:
        return f"{self.code} ({self.heading}): {self.description}"

    def asJson(self) -> IErrorInfo:
        """
        Convert the exception to JSON so it can be returned to the frontend

        ### Returns:
        * `IErrorInfo`: JSON
        """
        # Only include traceback if we're debugging
        if debug_active():
            trace = "\n".join(traceback.format_exception(self))
        else:
            trace = None
        return {
            "code": self.code,
            "heading": type(self).__name__,
            "description": self.description,
            "traceback": trace,
        }


class BadRequest(HTTPException):
    """
    The server cannot or will not process the request due to something that is
    perceived to be a client error (e.g., malformed request syntax, invalid
    request message framing, or deceptive request routing).
    """

    def __init__(
        self,
        description: str,
        traceback: Optional[str] = None,
    ) -> None:
        super().__init__(400, description, traceback)


class Unauthorized(HTTPException):
    """
    Although the HTTP standard specifies "unauthorized", semantically this
    response means "unauthenticated". That is, the client must authenticate
    itself to get the requested response.
    """

    def __init__(
        self,
        description: str,
        traceback: Optional[str] = None,
    ) -> None:
        super().__init__(401, description, traceback)


class Forbidden(HTTPException):
    """
    The client does not have access rights to the content; that is, it is
    unauthorized, so the server is refusing to give the requested resource.
    Unlike `Unauthorized`, the client's identity is known to the server.
    """

    def __init__(
        self,
        description: str,
        traceback: Optional[str] = None,
    ) -> None:
        super().__init__(403, description, traceback)


class NotFound(HTTPException):
    """
    The server can not find the requested resource. In the browser, this means
    the URL is not recognized. In an API, this can also mean that the endpoint
    is valid but the resource itself does not exist. Servers may also send this
    response instead of `403 Forbidden` to hide the existence of a resource
    from an unauthorized client. This response code is probably the most well
    known due to its frequent occurrence on the web.
    """

    def __init__(
        self,
        description: str,
        traceback: Optional[str] = None,
    ) -> None:
        super().__init__(404, description, traceback)


class MethodNotAllowed(HTTPException):
    """
    The request method is known by the server but is not supported by the
    target resource. For example, an API may not allow calling DELETE to remove
    a resource.
    """

    def __init__(
        self,
        description: str,
        traceback: Optional[str] = None,
    ) -> None:
        super().__init__(405, description, traceback)


class InternalServerError(HTTPException):
    """
    The server has encountered a situation it does not know how to handle.
    """

    def __init__(
        self,
        description: str,
        traceback: Optional[str] = None,
    ) -> None:
        super().__init__(500, description, traceback)


codes: dict[int, tuple[str, Optional[type[HTTPException]]]] = {
    200: ("Ok", None),
    400: ("Bad Request", BadRequest),
    401: ("Unauthorized", Unauthorized),
    403: ("Forbidden", Forbidden),
    404: ("Not Found", NotFound),
    405: ("Method Not Allowed", MethodNotAllowed),
    500: ("Internal Server Error", InternalServerError),
}
