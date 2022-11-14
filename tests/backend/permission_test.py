"""
# Tests / Backend / Permission Test

Tests to ensure permissions stay in sync.

If either of tests tests are failing, it is because the
resources/permissions.json file is not up-to-date.

You can fix this by running `python scripts/generate_permissions.py`
"""
import pytest
import json
from backend.models.permissions import Permission


@pytest.mark.core
def test_permissions_backend_to_json():
    """
    Are all permissions defined on the backend present in the JSON
    """
    with open("resources/permissions.json") as f:
        perms: dict = json.load(f)
    for p in Permission:
        key = str(p.value)
        assert key in perms.keys()
        assert perms[key]["name"] == p.name


@pytest.mark.core
def test_permissions_json_to_backend():
    """
    Are all permissions defined in the JSON present in the backend
    """
    with open("resources/permissions.json") as f:
        perms: dict = json.load(f)
    for p in perms:
        perm = Permission(int(p))
        assert perm.name == perms[p]["name"]
