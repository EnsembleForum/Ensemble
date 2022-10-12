"""
# Backend / Util / Auth check

Code for checking authentication
"""
import re
import requests
from . import http_errors


def do_auth_check(
    address: str,
    request_type: str,
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

    * `request_type` (`str`): request type (get, post)

    * `username_param` (`str`): username parameter name to use

    * `password_param` (`str`): password parameter name to use

    * `success_regex` (`str`): regular expression to check for success

    * `username` (`str`): username to check

    * `password` (`str`): password to check

    ### Returns:
    * `bool`: whether the authentication succeeded
    """
    try:
        match request_type.lower():
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
            case t:
                raise http_errors.BadRequest(f"Invalid request type {t}")
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
    try:
        return re.match(success_regex, res.text) is not None
    except re.error as e:
        raise http_errors.BadRequest(
            f"Invalid regular expression {success_regex}"
        ) from e
