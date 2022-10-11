import json
from flask import Flask, request


# Port where the app will run
PORT = 5812
AUTH_URL = f"http://localhost:{PORT}"

app = Flask('mock_auth')

# Load login data
logins: dict[str, str] = json.load(open("mock/auth/users.json"))


@app.get("/login")
def login():
    """
    Returns whether the login is valid

    ## Args:
    * `username` (`str`)
    * `password` (`str`)
    """
    username: str = request.args["username"]
    password: str = request.args["password"]
    try:
        if logins[username] == password:
            return "true"
    except KeyError:
        pass
    return "false"


@app.get("/")
def home():
    """
    Main page
    """
    return "mock.auth is up and running!"
