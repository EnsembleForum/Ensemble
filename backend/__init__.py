"""
# Ensemble Backend

A next-gen forum to make life easier for educators and students alike.

This is the main entrypoint to backend server.
"""
import os
from flask import Flask
from .routes import browse, debug, admin, auth, user
from .util import db_status

app = Flask(__name__)

# Initialise the database
db_status.init()

# Register blueprint routes
if os.getenv("ENSEMBLE_DEBUG") is not None:
    app.register_blueprint(debug, url_prefix="/debug")

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(browse, url_prefix="/browse")

# Main routes


@app.get("/")
def home():
    return "Hello, world! The Ensemble backend is up and running!"
