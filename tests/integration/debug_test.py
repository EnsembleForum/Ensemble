"""
# Tests / Integration / Debug Test

Tests for debug routes
"""
from .request.debug import echo, fail
from backend.util import http_errors


def test_echo():
    """Test that we can echo things"""
    assert echo("Hello, world") == {"value": "Hello, world"}


def test_fail():
    """Test that we can get an error 500 with the appropriate error info"""
    try:
        fail()
    except http_errors.InternalServerError as e:
        assert e.test_json is not None
        assert e.test_json["code"] == 500
        assert e.test_json["description"] == "You brought this upon yourself."
        assert e.test_json["heading"] == "Internal server error"
