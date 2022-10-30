"""
# Scripts / Clear

Send a simple clear request to the running server
"""
import _helpers
from backend.util.http_errors import HTTPException
import ensemble_request
import requests
import dotenv
import os
del _helpers

dotenv.load_dotenv('.flaskenv')

PORT = os.getenv('FLASK_RUN_PORT')
if PORT is None:
    raise RuntimeError("Unknown port")
URL = f"http://localhost:{PORT}"

try:
    ensemble_request.debug.clear()
except requests.ConnectionError:
    print("❗ Couldn't connect to server - is it running?")
    exit(1)
except requests.RequestException as e:
    print(f"❗ Request error while clearing: {e}")
    exit(1)
except HTTPException as e:
    print("❌ Failed to clear the database")
    print(e.heading)
    print(e.description)
    exit(1)


print("✅ Database cleared")
