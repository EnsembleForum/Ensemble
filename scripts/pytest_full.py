"""
# Scripts / Pytest backend

Runs pytest on the backend of the server
"""
from _helpers import backend, mock_auth, pytest

flask = backend(debug=True)
auth = mock_auth()
tests = pytest()

ret = tests.wait()
flask.terminate()
auth.terminate()

if ret:
    # Also write outputs to stdout
    print("❌ Tests failed")
else:
    print("✅ Tests passed! Good job!")
exit(ret)
