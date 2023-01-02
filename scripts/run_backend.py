"""
# Scripts / Run backend

Run the backend server
"""
import sys
from _helpers import backend, mock_auth, coverage_report

cov = "--coverage" in sys.argv

auth = mock_auth()
flask = backend(debug=True, auto_reload=True, live_output=True, coverage=cov)

try:
    flask.wait()
except KeyboardInterrupt:
    pass
flask.interrupt()
auth.interrupt()

if cov:
    print("☔ Waiting for coverage to clean up...")
    try:
        flask.wait()
        coverage_report()
    except KeyboardInterrupt:
        flask.kill()

print("\nGoodbye!")
