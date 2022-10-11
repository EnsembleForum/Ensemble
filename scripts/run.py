"""
# Scripts / Run

Run the server
"""
from _helpers import backend

flask = backend(debug=True)

try:
    exit(flask.wait())
except KeyboardInterrupt:
    flask.terminate()
    print("Goodbye!")
