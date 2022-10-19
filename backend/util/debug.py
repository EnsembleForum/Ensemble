"""
# Backend / Util / Debug

Code for interacting with the ENSEMBLE_DEBUG mode
"""
import os


def debug_active() -> bool:
    """
    Returns whether debugging is active

    This is True if the `ENSEMBLE_DEBUG` environment variable is set to
    `"TRUE"`.

    ### Returns:
    * `bool`: debug status
    """
    return os.getenv("ENSEMBLE_DEBUG") == "TRUE"
