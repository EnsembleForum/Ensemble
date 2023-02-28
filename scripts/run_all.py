"""
# Scripts / Run all

Run the backend and frontend servers
"""
import sys
from _helpers import backend, mock_auth, frontend

backend_url = None
debug = False
for var in sys.argv:
    if var.startswith("--backend="):
        backend_url = var.removeprefix("--backend=").strip()
    elif var == "--debug":
        debug = True


auth = mock_auth()
flask = backend(live_output=True, debug=debug)
npm = frontend(backend_url)

try:
    flask.wait()
except KeyboardInterrupt:
    pass

flask.interrupt()
npm.interrupt()
auth.interrupt()

print("\nGoodbye!")
