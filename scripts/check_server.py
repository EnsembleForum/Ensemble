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
    # Write all the outputs
    try:
        os.mkdir('output', )
    except FileExistsError:
        pass
    with open('output/server.stdout.txt', 'w') as out:
        out.write(flask.stdout.read().decode('utf-8'))
    with open('output/server.stderr.txt', 'w') as out:
        out.write(flask.stderr.read().decode('utf-8'))
    sys.exit(1)
else:
    print("✅ Server started")

# Finally, shut down the server
flask.terminate()
