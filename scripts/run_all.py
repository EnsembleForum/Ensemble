"""
# Scripts / Run all

Run the backend and frontend servers
"""
from _helpers import backend, mock_auth, frontend

auth = mock_auth()
flask = backend(live_output=True)
npm = frontend()

try:
    flask.wait()
except KeyboardInterrupt:
    pass

flask.interrupt()
npm.interrupt()
auth.interrupt()

print("\nGoodbye!")
