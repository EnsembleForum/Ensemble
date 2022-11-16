"""
# Scripts / Check start

Check that the server starts correctly, then exits
"""
from _helpers import backend

# Run and kill the backend
backend(debug=True).interrupt()
