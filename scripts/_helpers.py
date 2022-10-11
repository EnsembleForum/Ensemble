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


def write_outputs(process: subprocess.Popen[bytes], file: str | None):
    """
    Write program outputs to the output folder
    """
    # If no output file, write to stdout
    if file is None:
        print(f"Process {process.args!r}:")
        if process.stdout is not None:
            print("* stdout:")
            sys.stdout.write(process.stdout.read().decode('utf-8'))
        if process.stderr is not None:
            print("* stderr:")
            sys.stdout.write(process.stderr.read().decode('utf-8'))

    # Otherwise, write it to the requested files
    else:
        try:
            os.mkdir('output', )
        except FileExistsError:
            pass
        if process.stdout is not None:
            with open(f'output/{file}.stdout.txt', 'w') as out:
                out.write(process.stdout.read().decode('utf-8'))
        if process.stderr is not None:
            with open(f'output/{file}.stderr.txt', 'w') as out:
                out.write(process.stderr.read().decode('utf-8'))


def backend(debug=False):
    if debug:
        env = {"ENSEMBLE_DEBUG": "TRUE"}
        debug_flag = ["--debug"]
    else:
        env = {}
        debug_flag = []
    flask = subprocess.Popen(
        [sys.executable, '-u', '-m', 'flask', 'run'] + debug_flag,
        env=env,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    if flask.stderr is None or flask.stdout is None:
        print("❗ Can't read flask output", file=sys.stderr)
        flask.kill()
        sys.exit(1)

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
        write_outputs(flask, None)
        sys.exit(1)
    else:
        print("✅ Server started")
        return flask


def mock_login():
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
        login.kill()
        write_outputs(login, None)
        sys.exit(1)
    else:
        print("✅ Server started")
        return login


def pytest():
    pytest = subprocess.Popen(
        [sys.executable, '-u', '-m', 'pytest'],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # Wait for tests to finish
    print("🔨 Running tests...")
    ret = pytest.wait()
    write_outputs(pytest, "pytest")
    if ret == 0:
        print("✅ It works!")
        return True
    else:
        print("❌ Tests failed")
        return False
