"""
# Backend / Util / Auth check

Code for checking authentication
"""
import re
import requests
from typing import Literal
from . import http_errors


def do_auth_check(
    address: str,
    request_type: Literal['get', 'post', 'put', 'delete'],
    username_param: str,
    password_param: str,
    success_regex: str,
    username: str,
    password: str,
) -> bool:
    """
    Returns whether the authentication has worked for a particular user

    ### Args:
    * `address` (`str`): URL to request to

    * `request_type` (`str`): request type (get, post, put, delete)

    * `username_param` (`str`): username parameter name to use

    * `password_param` (`str`): password parameter name to use

    * `success_regex` (`str`): regular expression to check for success

    * `username` (`str`): username to check

    * `password` (`str`): password to check

    ### Returns:
    * `bool`: whether the authentication succeeded
    """
    try:
        match request_type:
            case "get":
                res = requests.get(
                    address,
                    params={
                        username_param: username,
                        password_param: password,
                    }
                )
            case "post":
                res = requests.post(
                    address,
                    json={
                        username_param: username,
                        password_param: password,
                    }
                )
            case "put":
                res = requests.put(
                    address,
                    json={
                        username_param: username,
                        password_param: password,
                    }
                )
            case "delete":
                res = requests.delete(
                    address,
                    params={
                        username_param: username,
                        password_param: password,
                    }
                )
    # Check for basic errors
    except requests.ConnectionError:
        raise http_errors.BadRequest(
            f"Unable to connect to {address} for login auth. Please double "
            f"check the address."
        )
    except requests.exceptions.InvalidSchema:
        raise http_errors.BadRequest(
            f"Invalid schema for {address} when checking login auth. Please "
            f"ensure your address contains the schema (such as http://)."
        )
    # Make sure the request worked properly
    if res.status_code != 200:
        c = res.status_code
        # Give helpful errors for the status code
        try:
            description = f"({http_errors.codes[c]})"
        except KeyError:  # pragma: no cover (we already cover most of them)
            description = ""
        raise http_errors.BadRequest(
            f"Auth server failed to process request - gave status code {c} "
            + description
        )

    try:
        return re.match(success_regex, res.text) is not None
    except re.error as e:
        raise http_errors.BadRequest(
            f"Invalid regular expression {success_regex}"
        ) from e
