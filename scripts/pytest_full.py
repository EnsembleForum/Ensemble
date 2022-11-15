"""
# Scripts / Pytest backend

Runs pytest on the backend of the server
"""
import sys
from _helpers import backend, mock_auth, pytest, Timer

cov = "--coverage" in sys.argv

t = Timer()

flask = backend(debug=True, coverage=cov)
auth = mock_auth()

with t:
    tests = pytest()
    ret = tests.wait()

flask.terminate()
auth.terminate()

if ret:
    # Also write outputs to stdout
    print("❌ Tests failed")
else:
    print(f"✅ Tests passed in {t.time:.2f} seconds! Good job!")
exit(ret)
