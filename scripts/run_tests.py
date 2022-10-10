"""
# Scripts / Run tests

Runs Pytest and server
"""
import dotenv
import os
import requests
import subprocess
import sys
import time

# Load environment variables
dotenv.load_dotenv('.flaskenv')

# Start flask
flask = subprocess.Popen(
    [sys.executable, '-u', '-m', 'flask', 'run'],
    env={"ENSEMBLE_DEBUG": "TRUE"},
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

if flask.stderr is None or flask.stdout is None:
    print("❗ Can't read flask output", file=sys.stderr)
    flask.kill()
    sys.exit(1)

# Start login server
login = subprocess.Popen(
    [sys.executable, '-u', '-m', 'mock.auth'],
    stderr=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
)

# Request until we get a success, but crash if we failed to start in 10 seconds
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
    sys.exit(1)
else:
    print("⛅ Server started")

pytest = subprocess.Popen(
    [sys.executable, '-u', '-m', 'pytest'],
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

# Wait for tests to finish
print("🔨 Running tests...")
ret = pytest.wait()

# Then shut down the server
flask.terminate()
login.terminate()

if pytest.stderr is None or pytest.stdout is None:
    print("❗ Can't read pytest output", file=sys.stderr)
    sys.exit(1)

# Write all the outputs
try:
    os.mkdir('output', )
except FileExistsError:
    pass
with open('output/server.stdout.txt', 'w') as out:
    out.write(flask.stdout.read().decode('utf-8'))
with open('output/server.stderr.txt', 'w') as out:
    out.write(flask.stderr.read().decode('utf-8'))
with open('output/pytest.stdout.txt', 'w') as out:
    out.write(pytest.stdout.read().decode('utf-8'))
with open('output/pytest.stderr.txt', 'w') as out:
    out.write(pytest.stderr.read().decode('utf-8'))

if ret == 0:
    print("✅ It works!")
else:
    print("❌ Tests failed")
exit(ret)
