"""
# Scripts / Run tests

Runs Pytest and server
"""
from _helpers import backend, pytest, write_outputs

flask = backend()

ret = pytest()

flask.terminate()

write_outputs(flask, 'flask')
if not ret:
    # Also write outputs to stdout
    write_outputs(flask, None)

exit(ret)
