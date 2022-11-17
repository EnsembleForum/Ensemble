"""
# Tests / Integration / Debug Test

Tests for debug routes
"""
import pytest
from ensemble_request.debug import echo, fail, enabled
from backend.util import http_errors


@pytest.mark.core
def test_echo():
    """Test that we can echo things"""
    assert echo("Hello, world") == {"value": "Hello, world"}


def test_enabled():
    """Make sure debugging is enabled"""
    assert enabled()["value"]


def test_fail():
    """Test that we can get an error 500 with the appropriate error info"""
    try:
        fail()
    except http_errors.InternalServerError as e:
        assert e.code == 500
        assert e.description == "You brought this upon yourself."
        assert e.heading == "Internal Server Error"
