
# Ensemble Backend

Code for running the backend of the program

## Running the backend

### For debugging

#### In VS Code

1. Start the server by choosing the "Backend & mock.auth" option in the Run and
   Debug panel.

3. Enjoy!

#### Outside of VS Code

With additional debugging tools including the mock auth server:

* `python scripts/run_backend.py`

Or without (you won't have access to `clear` or `echo` routes, or the mock
login server)

* `flask run`

### For testing

You can run all the tests using

`python scripts/pytest_backend.py`

This will send all the output to files in the `output/` directory.

### For deployment

TODO

## Structure

* Routes: contains blueprints for routes exposed by the API. Includes route
  logic.

* Models: definitions for classes and other data types used internally within
  the backend, possibly including code for database interaction?

* Types: definitions for types used by the API, used to help enforce return
  types for server routes, and to type check integration tests.

* Util: utility code (helper functions, useful decorators, etc).
