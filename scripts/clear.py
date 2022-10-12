"""
# Scripts / Clear

Send a simple clear request to the running server
"""
import requests
import dotenv
import os

dotenv.load_dotenv('.flaskenv')


PORT = os.getenv('FLASK_RUN_PORT')
if PORT is None:
    raise RuntimeError("Unknown port")
URL = f"http://localhost:{PORT}"

try:
    ret = requests.delete(f"{URL}/clear")
except requests.ConnectionError:
    print("❗ Couldn't connect to server - is it running?")
    exit(1)
except requests.RequestException as e:
    print(f"❗ Request error while clearing: {e}")
    exit(1)

if ret.status_code != 200:
    print("❌ Failed to clear the database")
    print(ret.text)
    exit(1)


print("✅ Database cleared")
