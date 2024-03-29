"""
# Scripts / Pytest backend core

Runs pytest on the backend of the server, but only for the core tests
"""
from _helpers import backend, mock_auth, pytest, Timer

t = Timer()

flask = backend(debug=True)
auth = mock_auth()

with t:
    tests = pytest(core=True)
    ret = tests.wait()

flask.interrupt()
auth.interrupt()

if ret:
    # Also write outputs to stdout
    print("❌ Tests failed")
else:
    print(f"✅ Tests passed in {t.time:.2f} seconds! Good job!")
exit(ret)
