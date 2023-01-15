
# A note on the authentication system

One of the core features of Ensemble is its use of an external authentication
system. It uses this in order to integrate with systems such as UNSW’s login
servers, which allows students to log in using their zID and password. This
also means that we can avoid some potential security flaws by not needing to
store user’s passwords directly. We expect that our target audience,
educational institutions, will already have an existing authentication system
that should be easy to integrate with Ensemble.

While it is possible to set up Ensemble to work with UNSW’s login system, we
understand that this could be seen as a security risk, given that the reader
would need to use their actual zID and password with our project. As such, we
have provided a mock authentication which behaves very similarly to UNSW’s
system, but with a small number of predefined users. For a mapping of these
users and their passwords, please refer to
[`mock/auth/users.json`](../../mock/auth/users.json). Each user’s password is
equal to their username. Note that this mock authentication server is not
secure and should not be used in a production environment.

Note that removing users from this file will cause our tests to fail.
