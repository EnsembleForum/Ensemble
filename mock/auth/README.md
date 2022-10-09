
# Mock / Auth

This is a simple web server which mocks an authentication server similar to the
one in use by UNSW.

## Running the server

The server is automatically run by the test script, but if you need to run it
manually, the following can be used.

`python -m mock.auth`

## Requesting to the server

Login requests can be made by get requesting to `http://localhost:5812/login`
with parameters `username` and `password`.

The server will return the string `"true"` if the login succeeds, and `"false"`
otherwise.

## User info

Login and password combinations can be found in `users.json`.
