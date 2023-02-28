
# The Ensemble Backend

We built our backend using Python 3.10, using the Flask web framework to build
our API, and Piccolo ORM to interact with our SQLite3 database. We also
supported external authentication that can integrate with UNSW’s
authentication system. In order to test our code and assure the quality of it,
we used Pytest, Coverage, Jestspectation, Mypy, and Flake8.

## Python

We built the backend using [Python](https://www.python.org/), as all of our
backend developers were familiar with it from COMP1531. This meant that less
time was spent learning the language, and more time building the project.
However, one disadvantage of this was that it was more difficult to integrate
the frontend with the backend. If we had used a TypeScript framework, we would
have been able to share our type definitions for the interface with the
frontend which would help them to develop and test their code more
efficiently, with the disadvantage being that we would need to spend more time
learning how to use a different framework. Although some of our developers had
some familiarity with Express, the additional learning curve would mean that
we would be more delayed with starting the project.

## Flask

Our backend used [Flask](https://github.com/pallets/flask) to build the API.
This was a good decision, as its unopinionated design meant that we could
structure our program to best suit our design goals. It was also a framework
that all of our backend developers were familiar with, meaning that once we
had built the basic structure for our project, we were all able to implement
routes quickly and without many issues.

## SQLite3

We used [SQLite](https://sqlite.org/index.html) as our database, as it is
fast, lightweight, and very popular for smaller projects. Although it isn’t as
scalable as other databases like PostgreSQL, the one-forum-per-instance design
for our server means that we don’t believe that it would ever need to grow to
the point where it becomes a bottleneck. We also benefited from the simple
setup process, since SQLite is provided with Python, which meant that no
additional installation was required. Originally, we planned to use
PostgreSQL, but we were unable to get it set up correctly after hours of work.
Our decision to use SQLite instead was massively beneficial.

## Piccolo ORM

We used [Piccolo ORM](https://github.com/piccolo-orm/piccolo) to pythonically
declare the structure of our database, as well as build and execute queries.
This was a very good decision, as it meant that our backend developer team,
who primarily weren’t familiar with databases were able to construct their
database queries more easily with the assistance of IDE Intellisense
predictions, and improved type safety. As this is a bleeding edge and
relatively new ORM, there were a few cases where we found minor bugs, however,
our bug reports were very quickly addressed, so this did not hinder our
development of the project. One feature of piccolo that we didn’t take
advantage of was its first-class support for async code. We decided that the
additional complexities of async would make it too slow for our team to learn,
and therefore we stuck to its synchronous functions. We would be able to get
significantly more performance for long-running routes (such as registering
users) if we implemented async, but we didn’t have time for it in the short
timeframe.

## Pytest

In order to test our backend, we wrote many integration tests using
[Pytest](https://github.com/pytest-dev/pytest). This was a very good decision as it meant that we were able to be certain that our backend was always working before we merged any pull request. However, towards the end of the project, our test suite had expanded to over 300 tests, and the test suite took over 10 minutes to run, which made the process of completing pull requests considerably slower for small fixes. In retrospect, we should have addressed this by only running the backend tests when there were changes to backend code, which would have prevented this issue for pull requests related to the frontend code or documentation. Towards the end of the project, we did take advantage of Pytest’s mark system to mark certain tests as “core” tests, which would be run before the other tests, so that we could get a quick idea of what was or wasn’t working without waiting for the full test suite.

## Coverage

We also used [coveragepy](https://github.com/nedbat/coveragepy) to measure the
effectiveness of our tests, which helped us identify areas where our tests
weren’t especially effective, thereby uncovering some minor bugs in our
implementation. By the end of the project, we had 98% code coverage, which
helped assure us that our code was correct.

## Jestspectstion

During the late stages of the project, we realised that checking the complex
data structures used by our API was making our tests difficult to read, so a
team member spent some time implementing a library named
[Jestspectation](https://github.com/MiguelGuthridge/Jestspectation) to allow
us to test data in a readable structure. Although this did improve the
readability of our tests, it was done too late for it to be widely adopted
throughout our entire test suite. If we had done this sooner, we would have
benefited from this sooner.

## Mypy

We statically typed the entire backend using
[Mypy](https://github.com/python/mypy), which allowed us to get much better
editor suggestions, as well as static reassurance that our code is correct.
Although
[some bugs in its analysis](https://github.com/python/mypy/issues/11065)
prevented us from using some of Python’s features, it was mostly beneficial
for our code quality and development speed, especially given the size of the
codebase.

## Flake8

We used [Flake8](https://github.com/PyCQA/flake8) to lint our Python code.
This helped us ensure that we had a relatively consistent style for our code,
and prevented readability issues and some simple bugs. We decided not to use a
more opinionated linter such as Black, as the constraints it would place on
our code style would have been frustrating.

## Backend project structure

We split our backend into a variety of modules to ensure that our code was
loosely coupled, but still cohesive.

### Models

The models module was used to define our database structure using Piccolo
within tables.py, as well as creating wrappers around the tables in order to
wrap around the database queries so that our route code could interact with a
simple, type-safe wrapper around the database queries. This had the advantage
of allowing us to write code that was more concise, with more checks being
performed in the background - for example a 400 response was automatically
returned if a database lookup ever failed. One disadvantage this had was that
our design reduced the performance of the code significantly, as many more
database queries would usually be performed per operation than was necessary.

If we had more time, we would refactor our code so that instances of our model
classes always held a reference to the table row rather than looking it up
every time an operation was performed.

### Routes

Our API routes were defined in the routes module, which allowed us to keep the
API logic separated from the logic of our models.

### Types

In the types module, we defined type definitions for all of our API routes,
which could then be used by both the server and the API requests helpers to
provide type safety for all of our data structures. In particular, we
implemented subclasses of the int type to prevent mingling between IDs of
incorrect types (eg returning a post ID instead of a user ID).

### Util

We defined utility helper functions in the util module. This includes
supporting code for interacting with the authentication server, code for
validating tokens, code for performing common database queries, as well as any
more useful things.
