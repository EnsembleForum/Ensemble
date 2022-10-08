import os


PORT = os.getenv('FLASK_RUN_PORT')
if PORT is None:
    raise RuntimeError("Unknown port")
URL = f"http://localhost:{PORT}"
