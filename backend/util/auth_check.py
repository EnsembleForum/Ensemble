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
    if request_type == "get":
        res = requests.get(
            address,
            params={
                username_param: username,
                password_param: password,
            }
        )
    else:
        res = requests.post(
            address,
            json={
                username_param: username,
                password_param: password,
            }
        )
    try:
        return re.match(success_regex, res.text) is not None
    except re.error as e:
        raise http_errors.BadRequest(
            f"Invalid regular expression {success_regex}"
        ) from e
