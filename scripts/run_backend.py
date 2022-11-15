"""
# Scripts / Run

Run the server
"""
import sys
from _helpers import backend, mock_auth

cov = "--coverage" in sys.argv

auth = mock_auth()
flask = backend(debug=True, auto_reload=True, live_output=True, coverage=cov)

try:
    flask.wait()
except KeyboardInterrupt:
    pass
flask.interrupt()
auth.interrupt()
print("\nGoodbye!")
