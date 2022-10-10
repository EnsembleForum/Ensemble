"""
# Backend / Util / Exceptions

Exceptions used by the Ensemble backend - many of these inherit from
http_errors, but can be used to indicate specific things that happened, so we
don't accidentally catch exceptions we don't want to.
"""
from . import http_errors


class IdNotFound(http_errors.BadRequest):
    """
    Couldn't find an entry with ID in the database.

    Extends `BadRequest`
    """


class MatchNotFound(http_errors.BadRequest):
    """
    Couldn't find an entry with matching info in the database.

    Extends `BadRequest`
    """


class InvalidInput(http_errors.BadRequest):
    """
    An input was invalid (eg a text field that needed > 0 chars)

    Extends `BadRequest`
    """


class PermissionError(http_errors.Forbidden):
    """
    User doesn't have permission to perform a certain action.

    Extends `Forbidden`
    """


class AuthenticationError(http_errors.Forbidden):
    """
    User failed to authenticate (usually invalid token).

    Extends `Forbidden`
    """
