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
from typing import Optional
# Add the top directory to the path so Python doesn't have a hissy fit
sys.path.append(str(Path(__file__).parent.parent))
import dotenv
import os
import requests
import sys
import time
from subtask import Subtask

# Load environment variables
dotenv.load_dotenv('.flaskenv')


def output_folder():
    try:
        os.mkdir('output', )
    except FileExistsError:
        pass


class Timer:
    def __init__(self) -> None:
        self.__time_started = 0.
        self.time: float | None = None

    def __enter__(self) -> None:
        self.__time_started = time.perf_counter()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.time = time.perf_counter() - self.__time_started


def backend(debug=False, auto_reload=False, live_output=False, coverage=False):
    def started() -> bool:
        try:
            requests.get(
                f'http://localhost:{os.getenv("FLASK_RUN_PORT")}/debug/echo',
                params={'value': 'Test script startup...'},
            )
            return True
        except requests.ConnectionError:
            return False

    if started():
        print("❗ Server already running")
        sys.exit(1)

    if debug:
        env = {"ENSEMBLE_DEBUG": "TRUE"}
        print("🔨 Debugging enabled")
    else:
        env = None
    if auto_reload:
        debug_flag = ["--debug"]
        print("🔁 Auto reload enabled")
    else:
        debug_flag = []
    if coverage:
        cov_flag = ["coverage", "run", "-m"]
        print("☔ Coverage enabled")
    else:
        cov_flag = []
    flask = Subtask(
        [sys.executable, '-u', '-m'] + cov_flag + ['flask'] + debug_flag + ['run'],
        live_output,
        env,
        started
    )
    if flask.poll() is not None:
        print("❗ Server crashed during startup")
        sys.exit(1)
    print("✅ Backend started")
    return flask


def mock_auth():

    def started() -> bool:
        try:
            requests.get('http://localhost:5812/')
            return True
        except requests.ConnectionError:
            return False

    login = Subtask(
        [sys.executable, '-u', '-m', 'mock.auth'],
        wait_for=started
    )
    print("✅ mock.auth started")
    return login


def pytest(core = False):
    if core:
        marks = ['-m', 'core']
        app = "Pytest (core)"
    else:
        marks = []
        app = "Pytest"
    t = Subtask(
        [sys.executable, '-u', '-m', 'pytest'] + marks,
    )
    print(f"🔨 {app} started")
    return t


def coverage_report():
    Subtask(
        [sys.executable, '-u', '-m', 'coverage', 'report'],
        live_output=True
    ).wait()


def frontend(backend_url: Optional[str] = None):
    print("✅ Frontend starting")
    if backend_url is not None:
        env = {
            "backend_url": backend_url,
        }
    else:
        env = {}
    return Subtask(
        ['npm', 'start'],
        env=env
    )
