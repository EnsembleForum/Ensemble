
# Backend

Code for running the backend of the program

## Running the backend

### For debugging

With additional debugging tools (recommended):

`ENSEMBLE_DEBUG=TRUE flask --debug run`

Or without

`flask run`

### For deployment

TODO

## Structure

* Routes: contains blueprints for routes exposed by the API. Includes route
  logic.

* Models: definitions for classes and other data types used internally within
  the backend, possibly including code for database interaction?

* Types: definitions for types used by the API, used to help enforce return
  types for server routes.

* Util: utility code (helper functions, useful decorators, etc).
