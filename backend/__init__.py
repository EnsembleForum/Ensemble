"""
# Ensemble Backend

A next-gen forum to make life easier for educators and students alike.

This is the main entrypoint to backend server.
"""
from flask import Flask
from .routes import debug

app = Flask(__name__)

# Register blueprint routes
app.register_blueprint(debug, url_prefix='/debug')


# Main routes
@app.get('/')
def home():
    return 'Hello, world! The Ensemble backend is up and running!'
