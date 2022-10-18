"""
# Scripts / Run

Run the server
"""
from _helpers import backend, mock_auth

auth = mock_auth()
flask = backend(debug=True, live_output=True)

try:
    flask.wait()
except KeyboardInterrupt:
    pass
flask.terminate()
auth.terminate()
print("\nGoodbye!")
