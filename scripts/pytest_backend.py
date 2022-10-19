"""
# Scripts / Test

Runs pytest on the backend of the server
"""
from _helpers import backend, mock_auth, pytest, write_outputs

flask = backend(debug=True)

auth = mock_auth()

try:
    ret = pytest()
except KeyboardInterrupt:
    print("❗ Testing cancelled")
    flask.terminate()
    auth.terminate()
    write_outputs(flask, 'flask')
    exit(1)

flask.terminate()
auth.terminate()

write_outputs(flask, 'flask')
if ret:
    # Also write outputs to stdout
    write_outputs(flask, None)

exit(ret)
