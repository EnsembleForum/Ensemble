"""
tests > backend > conftest

Configuration for tests
"""
import pytest
from tests.integration.functions.debug import clear


@pytest.fixture(autouse=True)
def before_each():
    """Clear the database between tests"""
    clear()
