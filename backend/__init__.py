"""
Ensemble

A next-gen forum to make life easier for educators and students alike.

This is the main entrypoint to the program.
"""
import sys
from flask import Flask

app = Flask(__name__)


@app.get('/')
def home():
    return "Hello, world!"
