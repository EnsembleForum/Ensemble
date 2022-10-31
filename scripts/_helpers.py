"""
# Scripts / _helpers

Helper code for the scripts
"""
# flake8: noqa
# Currently there is no way to ignore specific errors, so we just need to
# ignore everything - be careful editing this file, since Flake8 won't pick up
# on anything as a result of this.
# If we find a way, ignore E402 (import not at top of file)

import sys
from pathlib import Path
# Add the top directory to the path so Python doesn't have a hissy fit
sys.path.append(str(Path(__file__).parent.parent))
import dotenv
import os
import requests
import subprocess
import sys
import time
from typing import Callable

# Load environment variables
dotenv.load_dotenv('.flaskenv')


def output_folder():
    try:
        os.mkdir('output', )
    except FileExistsError:
        pass


class Task:
    def __init__(
        self,
        name: str,
        args: list[str],
        live_output: bool = False,
        env: dict[str, str] = None,
        wait_for: Callable[[], bool] = None,
    ):
        self.process = None
        curr_env = os.environ.copy()
        if env is not None:
            curr_env.update(env)
        output_folder()
        if live_output:
            self.stdout = None
            self.stderr = None
        else:
            self.stdout = open(f"output/{name}.stdout.txt", 'w')
            self.stderr = open(f"output/{name}.stderr.txt", 'w')
        self.process = subprocess.Popen(
            args,
            stdout=self.stdout,
            stderr=self.stderr,
            env=curr_env
        )
        if wait_for is not None:
            # Request until we get a success, but crash if we failed to start
            # in 10 seconds
            start_time = time.time()
            started = False
            while time.time() - start_time < 10:
                if wait_for():
                    started = True
                    break
            if not started:
                print(f"❗ {name} failed to start in time")
                sys.exit(1)

    def __del__(self):
        # Always kill the subprocess when this goes out of scope
        self.kill()

    def close_files(self):
        if self.stdout is not None:
            self.stdout.close()
        if self.stderr is not None:
            self.stderr.close()

    def terminate(self):
        if self.process is not None:
            self.process.terminate()
        self.close_files()

    def kill(self):
        if self.process is not None:
            self.process.kill()
        self.close_files()

    def wait(self):
        if self.process is None:
            raise ValueError("Process not started")
        ret = self.process.wait()
        self.close_files()
        return ret

    def poll(self):
        if self.process is None:
            raise ValueError("Process not started")
        ret = self.process.poll()
        if ret is not None:
            self.close_files()
        return ret


def backend(debug=False, live_output=False):
    def started() -> bool:
        try:
            requests.get(
                f'http://localhost:{os.getenv("FLASK_RUN_PORT")}/debug/echo',
                params={'value': 'Test script startup...'},
            )
            return True
        except requests.ConnectionError:
            return False

    if debug:
        env = {"ENSEMBLE_DEBUG": "TRUE"}
        debug_flag = ["--debug"]
    else:
        debug_flag = []
        env = None
    flask = Task(
        'backend',
        [sys.executable, '-u', '-m', 'flask'] + debug_flag + ['run'],
        live_output,
        env,
        started
    )
    if flask.poll() is not None:
        print("❗ Server crashed during startup")
        sys.exit(1)
    print("✅ Server started")
    return flask


def mock_auth():

    def started() -> bool:
        try:
            requests.get('http://localhost:5812/')
            return True
        except requests.ConnectionError:
            return False

    login = Task(
        'mock.auth',
        [sys.executable, '-u', '-m', 'mock.auth'],
        wait_for=started
    )
    print("✅ mock.auth started")
    return login


def pytest():
    t = Task(
        'pytest',
        [sys.executable, '-u', '-m', 'pytest'],
    )
    print("🔨 Pytest started")
    return t
