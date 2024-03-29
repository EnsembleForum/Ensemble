"""
# Request

Contains code used for requesting routes available on the backend. This is used
for testing, and for generating documentation of the available routes.

## Primary routes:

* `admin`: routes used for administration

* `auth`: routes related to authorisation

* `browse`: routes related to browsing the forum

* `debug`: routes used to debug the server outside of a production environment

* `taskboard`: routes used it interact with the taskboard view

* `user`: routes used to interact with user profiles
"""
# Load .flaskenv file to sort out environment variables
from dotenv import load_dotenv
load_dotenv(".flaskenv")
del load_dotenv


from . import (  # noqa: E402
    admin,
    auth,
    browse,
    debug,
    taskboard,
    user,
    notifications,
)

__all__ = [
    'admin',
    'auth',
    'browse',
    'debug',
    'taskboard',
    'user',
    'notifications',
]
