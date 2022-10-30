"""
# Scripts / Clear

Send a simple clear request to the running server
"""
import ensemble_request
import requests
import dotenv
import os

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
except Exception as e:
    print("❌ Failed to clear the database")
    print(e.text)
    exit(1)


print("✅ Database cleared")
