"""
# Backend / Util / Email validator

Contains the definition for an email validator
"""
import re
from . import http_errors

EMAIL_REGEX = re.compile(
    r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"  # noqa: E501
)


def assert_email_valid(email: str):
    """
    If the given email is not valid, a BadRequest is raised
    """
    if EMAIL_REGEX.match(email) is None:
        raise http_errors.BadRequest(f"Email {email} is not valid")


def assert_name_valid(name: str, name_type: str = "Name"):
    """
    If the given name is not valid (0 chars), a BadRequest is raised
    """
    if len(name) == 0:
        raise http_errors.BadRequest(f"{name_type} cannot be empty")


def assert_heading_valid(heading: str):
    """
    If the given heading is not valid (0 chars), a BadRequest is raised
    """
    if len(heading) == 0:
        raise http_errors.BadRequest("Heading of a post cannot be empty")


def assert_text_valid(text: str, text_type: str):
    """
    If the given text is not valid (0 chars), a BadRequest is raised
    """
    if len(text) == 0:
        raise http_errors.BadRequest(f"Text of a {text_type} cannot be empty")
