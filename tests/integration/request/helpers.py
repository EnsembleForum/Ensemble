import json
import requests
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


def get(url: str, params: dict) -> dict:
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
    ))


def post(url: str, body: dict) -> dict:
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
    ))


def put(url: str, body: dict) -> dict:
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
    ))


def delete(url: str, params: dict) -> dict:
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
    ))
