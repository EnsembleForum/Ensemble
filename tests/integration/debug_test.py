"""
# Tests / Integration / Debug Test

Tests for debug routes
"""
from .request.debug import echo


def test_echo():
    """Test that we can echo things"""
    assert echo("Hello, world") == {"value": "Hello, world"}
