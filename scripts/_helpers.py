"""
# Scripts / _helpers

Helper code for the scripts
"""
import dotenv
import os
import requests
import subprocess
import sys
import time

# Load environment variables
dotenv.load_dotenv('.flaskenv')


def write_outputs(
    process: str,
    stdout: str | None,
    stderr: str | None,
    file: str | None,
):
    """
    Write program outputs to the output folder
    """
    # If no output file, write to stdout
    if file is None:
        print(f"Process {process}:")
        if stdout is not None:
            print("* stdout:")
            sys.stdout.write(stdout)
            print()
        if stderr is not None:
            print("* stderr:")
            sys.stdout.write(stderr)
            print()

    # Otherwise, write it to the requested files
    else:
        try:
            os.mkdir('output', )
        except FileExistsError:
            pass
        if stdout is not None:
            with open(f'output/{file}.stdout.txt', 'w') as out:
                out.write(stdout)
        if stderr is not None:
            with open(f'output/{file}.stderr.txt', 'w') as out:
                out.write(stderr)


def backend(debug=False, live_output=False):
    env = os.environ.copy()
    if debug:
        env.update({"ENSEMBLE_DEBUG": "TRUE"})
        debug_flag = ["--debug"]
    else:
        debug_flag = []
    if live_output is False:
        outputs = subprocess.PIPE
    else:
        outputs = None
    flask = subprocess.Popen(
        [sys.executable, '-u', '-m', 'flask'] + debug_flag + ['run'],
        env=env,
        stderr=outputs,
        stdout=outputs,
    )

    # Request until we get a success, but crash if we failed to start in 10
    # seconds
    start_time = time.time()
    started = False
    while time.time() - start_time < 10:
        try:
            requests.get(
                f'http://localhost:{os.getenv("FLASK_RUN_PORT")}/debug/echo',
                params={'value': 'Test script startup...'},
            )
        except requests.ConnectionError:
            continue
        started = True
        break

    if not started:
        print("❗ Server failed to start in time")
        flask.kill()
        if outputs is not None:
            o, e = flask.communicate()
            write_outputs(repr(flask), o.decode(), e.decode(), None)
        sys.exit(1)
    else:
        if flask.poll() is not None:
            print("❗ Server crashed during startup")
            if outputs is not None:
                write_outputs(repr(flask), o.decode(), e.decode(), None)
            sys.exit(1)
        print("✅ Server started")
        return flask


def mock_auth():
    login = subprocess.Popen(
        [sys.executable, '-u', '-m', 'mock.auth'],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    if login.stderr is None or login.stdout is None:
        print("❗ Can't read flask output", file=sys.stderr)
        login.kill()
        sys.exit(1)

    # Request until we get a success, but crash if we failed to start in 10
    # seconds
    start_time = time.time()
    started = False
    while time.time() - start_time < 10:
        try:
            requests.get('http://localhost:5812/')
        except requests.ConnectionError:
            continue
        started = True
        break

    if not started:
        print("❗ mock.auth failed to start in time")
        login.kill()
        sys.exit(1)
    else:
        print("✅ mock.auth started")
        return login


def pytest():
    t = subprocess.Popen(
        [sys.executable, '-u', '-m', 'pytest'],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    print("🔨 Pytest started")
    return t
