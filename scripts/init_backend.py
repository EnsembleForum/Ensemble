"""
# Scripts / init-backend-script

Send a default setup request to the server to register an admin
"""
import _helpers
from backend.util.http_errors import HTTPException
import ensemble_request
import requests
import dotenv
import os
import clear
del _helpers
del clear

dotenv.load_dotenv('.flaskenv')


PORT = os.getenv('FLASK_RUN_PORT')
if PORT is None:
    raise RuntimeError("Unknown port")
URL = f"http://localhost:{PORT}"

try:
    ret = ensemble_request.admin.init(
        address="http://localhost:5812/login",
        request_type="get",
        username_param="username",
        password_param="password",
        success_regex="true",
        username="admin1",
        password="admin1",
        email="admin1@example.com",
        name_first="Bophades",
        name_last="Nuts",
        pronoun = "he/him",
    )
except requests.ConnectionError:
    print("❗ Couldn't connect to server - is it running?")
    exit(1)
except requests.RequestException as e:
    print(f"❗ Request error while initialising: {e}")
    exit(1)
except HTTPException as e:
    print("❌ Failed to initialise the backend")
    print(e.heading)
    print(e.description)
    exit(1)


print("✅ Backend initialised")
