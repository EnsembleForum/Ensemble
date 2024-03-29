"""
# Ensemble Backend

A next-gen forum to make life easier for educators and students alike.

This is the main entrypoint to backend server.
"""
from flask import Flask
from flask_cors import CORS  # type: ignore
from werkzeug.exceptions import HTTPException as WzException
from .routes import (
    debug, admin, auth, user, browse, taskboard, notifications, tags
)
from .util import db_status
from .util.http_errors import HTTPException
from .util.error_handler import (
    http_error_handler,
    general_error_handler,
    werkzeug_error_handler,
)

app = Flask(__name__)
CORS(app)

# Register error handlers
app.register_error_handler(HTTPException, http_error_handler)
app.register_error_handler(Exception, general_error_handler)
app.register_error_handler(WzException, werkzeug_error_handler)

# Initialise the database
db_status.init()

# Register blueprint routes
app.register_blueprint(debug, url_prefix="/debug")
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(browse, url_prefix="/browse")
app.register_blueprint(taskboard, url_prefix="/taskboard")
app.register_blueprint(notifications, url_prefix="/notifications")
app.register_blueprint(tags, url_prefix="/tags")


# Main routes
@app.get("/")
def home():
    return "Hello, world! The Ensemble backend is up and running!"
