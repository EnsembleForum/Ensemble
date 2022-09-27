"""
# Backend / Util / HTTP Errors

Definitions for HTTP exceptions used by the server

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
from werkzeug.exceptions import HTTPException


class BadRequest(HTTPException):
    """
    The server cannot or will not process the request due to something that is
    perceived to be a client error (e.g., malformed request syntax, invalid
    request message framing, or deceptive request routing).
    """
    code = 400


class Unauthorized(HTTPException):
    """
    Although the HTTP standard specifies "unauthorized", semantically this
    response means "unauthenticated". That is, the client must authenticate
    itself to get the requested response.
    """
    code = 401


class Forbidden(HTTPException):
    """
    The client does not have access rights to the content; that is, it is
    unauthorized, so the server is refusing to give the requested resource.
    Unlike `Unauthorized`, the client's identity is known to the server.
    """
    code = 403
