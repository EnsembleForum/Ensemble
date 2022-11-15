"""
# Scripts / Run

Run the server
"""
import sys
from _helpers import backend, mock_auth

cov = "--coverage" in sys.argv

auth = mock_auth()
flask = backend(debug=True, live_output=True, coverage=cov)

try:
    flask.wait()
except KeyboardInterrupt:
    pass
flask.terminate()
auth.terminate()
print("\nGoodbye!")
