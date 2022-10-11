"""
# Scripts / Run tests

Runs Pytest and server
"""
from _helpers import backend, mock_auth, pytest, write_outputs

flask = backend(debug=True)

auth = mock_auth()

ret = pytest()

flask.terminate()
auth.terminate()

write_outputs(flask, 'flask')
if ret:
    # Also write outputs to stdout
    write_outputs(flask, None)

exit(ret)
