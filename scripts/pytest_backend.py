"""
# Scripts / Test

Runs pytest on the backend of the server
"""
from _helpers import backend, mock_auth, pytest, write_outputs
from subprocess import TimeoutExpired

flask = backend(debug=True)
tests = pytest()
auth = mock_auth()

flask_out = ''
flask_err = ''
tests_out = ''
tests_err = ''

try:
    while True:
        try:
            o, e = flask.communicate(timeout=3)
            if o is not None:
                flask_out += o.decode()
            if e is not None:
                flask_err += e.decode()
        except TimeoutExpired:
            pass
        try:
            o, e = tests.communicate(timeout=3)
            if o is not None:
                tests_out += o.decode()
            if e is not None:
                tests_err += e.decode()
        except TimeoutExpired:
            pass
        if tests.poll() is not None:
            break
        if flask.poll() is not None:
            print("❗ Backend quit unexpectedly")
            exit(1)
except KeyboardInterrupt:
    print("❗ Testing cancelled")
    flask.terminate()
    auth.terminate()
    tests.terminate()
    o, e = flask.communicate(timeout=3)
    if o is not None:
        flask_out += o.decode()
    if e is not None:
        flask_err += e.decode()
    o, e = tests.communicate(timeout=3)
    if o is not None:
        tests_out += o.decode()
    if e is not None:
        tests_err += e.decode()
    write_outputs(repr(flask), flask_out, flask_err, None)
    write_outputs(repr(tests), tests_out, tests_err, None)
    exit(1)

flask.terminate()
auth.terminate()
ret = tests.poll()

o, e = flask.communicate(timeout=3)
if o is not None:
    flask_out += o.decode()
if e is not None:
    flask_err += e.decode()
o, e = tests.communicate(timeout=3)
if o is not None:
    tests_out += o.decode()
if e is not None:
    tests_err += e.decode()

write_outputs(repr(flask), flask_out, flask_err, 'flask')
write_outputs(repr(tests), tests_out, tests_err, 'pytest')
if ret:
    # Also write outputs to stdout
    write_outputs(repr(flask), flask_out, flask_err, None)
    write_outputs(repr(tests), tests_out, tests_err, None)
    print("❌ Tests failed")
else:
    print("✅ Tests passed! Good job!")
exit(ret)
