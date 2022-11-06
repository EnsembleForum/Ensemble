"""
# Tests / Scripts test

Tests for the utility scripts (within reason). This should help ensure they
don't break if we randomly refactor.

* Clear script
* Init script
* Generate routes
"""
from backend.util.http_errors import Forbidden
from pathlib import Path
import pytest
import shutil
import subprocess
import sys
import ensemble_request
from mock.auth import AUTH_URL


def test_clear():
    """Does the clear script work correctly?"""
    ensemble_request.debug.clear()
    # Initialise the database and test it gets cleared
    usr = ensemble_request.admin.init(
        address=f"{AUTH_URL}/login",
        request_type="get",
        username_param="username",
        password_param="password",
        success_regex="true",
        username='admin1',
        password='admin1',
        email='someone@example.com',
        name_first="Whos",
        name_last="Joe",
        pronoun="he/him",
    )
    code = subprocess.Popen(
        [sys.executable, 'scripts/clear.py'],
    ).wait()
    assert code == 0
    # When the database is cleared, our data is deleted
    # meaning our token is invalidated
    with pytest.raises(Forbidden):
        ensemble_request.user.profile(usr["token"], usr["user_id"])


def test_init():
    """
    Does the init script initialise the server, allowing us to login as
    admin1?
    """
    code = subprocess.Popen(
        [sys.executable, 'scripts/init_backend.py'],
    ).wait()
    assert code == 0
    ensemble_request.auth.login('admin1', 'admin1')


def test_routes():
    """
    Does the routes script generate routes for the API?
    """
    code = subprocess.Popen(
        [sys.executable, 'scripts/routes.py', 'route_docs'],
    ).wait()
    assert code == 0
    p = Path('route_docs')
    assert p.exists()
    assert p.is_dir()
    shutil.rmtree(p)
