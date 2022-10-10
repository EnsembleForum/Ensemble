import json
import requests
from backend.types.auth import JWT
from backend.util import http_errors


def handle_response(response: requests.Response) -> dict:
    """
    Parse response to a request
    """
    match response.status_code:
        case 200:
            try:
                loaded = json.loads(response.text)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in response: {e}")
            if not isinstance(loaded, dict):
                raise ValueError(
                    f"Invalid response: expected dictionary, got {loaded}")
            return loaded
        case 400:
            raise http_errors.BadRequest(response.text)
        case 401:
            raise http_errors.Unauthorized(response.text)
        case 403:
            raise http_errors.Forbidden(response.text)
        case 404:
            raise http_errors.NotFound(response.url)
        case 405:
            raise http_errors.MethodNotAllowed(response.request.method)
        case 500:
            raise http_errors.InternalServerError(response.text)
        case i:
            raise ValueError(f"Unrecognised status code: {i}")


def encode_headers(token: JWT | None) -> dict[str, str]:
    """
    Returns an object representing the headers used in the request

    This encodes the token if present

    ### Args:
    * `token` (`JWT | None`): token if present

    ### Returns:
    * `dict[str, str]`: headers
    """
    if token is None:
        return {}
    else:
        return {"token": token}


def get(token: JWT | None, url: str, params: dict) -> dict:
    """
    Returns the response to a GET web request

    This also parses the response to help with error checking

    ### Args:
    * `url` (`str`): URL to request to

    * `params` (`dict`): parameters to send

    ### Returns:
    * `dict`: response data
    """
    return handle_response(requests.get(
        url,
        params=params,
        headers=encode_headers(token),
    ))


def post(token: JWT | None, url: str, body: dict) -> dict:
    """
    Returns the response to a POST web request

    This also parses the response to help with error checking

    ### Args:
    * `url` (`str`): URL to request to

    * `body` (`dict`): body to send

    ### Returns:
    * `dict`: response data
    """
    return handle_response(requests.post(
        url,
        json=body,
        headers=encode_headers(token),
    ))


def put(token: JWT | None, url: str, body: dict) -> dict:
    """
    Returns the response to a PUT web request

    This also parses the response to help with error checking

    ### Args:
    * `url` (`str`): URL to request to

    * `body` (`dict`): body to send

    ### Returns:
    * `dict`: response data
    """
    return handle_response(requests.put(
        url,
        json=body,
        headers=encode_headers(token),
    ))


def delete(token: JWT | None, url: str, params: dict) -> dict:
    """
    Returns the response to a DELETE web request

    This also parses the response to help with error checking

    ### Args:
    * `url` (`str`): URL to request to

    * `params` (`dict`): parameters to send

    ### Returns:
    * `dict`: response data
    """
    return handle_response(requests.delete(
        url,
        params=params,
        headers=encode_headers(token),
    ))
