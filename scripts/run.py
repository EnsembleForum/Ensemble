"""
# Scripts / Run

Run the server
"""
from _helpers import backend

flask = backend()

try:
    exit(flask.wait())
except KeyboardInterrupt:
    flask.terminate()
    print("Goodbye!")
