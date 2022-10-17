"""
# Tests / Integration / Debug Test

Tests for debug routes
"""
from .request.debug import echo, fail
from backend.util import http_errors
from backend.types.errors import IErrorInfo
from typing import cast


def test_echo():
    """Test that we can echo things"""
    assert echo("Hello, world") == {"value": "Hello, world"}


def test_fail():
    """Test that we can get an error 500 with the appropriate error info"""
    try:
        fail()
    except http_errors.InternalServerError as e:
        # TODO: Make this nicer - some proper exception matching would be super
        # helpful
        err = cast(http_errors.InternalServerError[IErrorInfo], e)
        assert e.test_json is not None
        assert err.test_json["code"] == 500
        assert err.test_json["description"] \
            == "You brought this upon yourself."
        assert err.test_json["heading"] == "Internal server error"
