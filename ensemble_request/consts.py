"""
# Requests / Consts

Constants used when testing
"""
import os


PORT = os.getenv('FLASK_RUN_PORT')
"""The port that the backend is running on"""

if PORT is None:
    raise RuntimeError("Unknown port")

URL = f"http://localhost:{PORT}"
"""The URL through which the server can be accessed for testing"""
