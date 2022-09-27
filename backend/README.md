
# Backend

Code for running the backend of the program

## Running the backend

### For debugging

`flask -app backend --debug run`

### For deployment

TODO

## Structure

* Routes: contains blueprints for routes exposed by the API.

* Logic: contains the logic behind the routes.

* Models: definitions for classes and other data types used by the logic,
  possibly including stuff for database interaction?

* Util: utility code (helper functions, useful decorators, etc).
