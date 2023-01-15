
# Forum setup

In order to function correctly, a small amount of configuration is required to
use Ensemble. Upon starting the frontend, the website will open to a page
where you need to enter a few settings. In particular, you need to specify the
method for communicating with the authentication server, as well as provide
the details of the first user. This information is pre-filled to work with the
mock authentication server, but can be changed as required to link to a
different authentication server.

| Value   | Meaning | Default |
| ------- | ------- | ------- |
| Address | Address to send authentication requests to. | `http://localhost:5812/login` |
| Request type | Kind of request to send. | `GET` |
| Username param | The name of the parameter to use for the username. | `username` |
| Password param | The name of the parameter to use for the password. | `password` |
| Success regex | A regular expression to match the output of the authentication server. If the returned document matches, the login will be considered successful. | `true` |

For example, given the default values, Ensemble will send the following
request:

```txt
GET http://localhost:5812/login?username=myuser&password=mypassword
```

If the authentication server returns `true`, then the login will be considered
a success.

Upon submitting the form, you should be taken to the main page of the forum.
At this point, you will likely want to navigate to the administrator options
to register more users.
