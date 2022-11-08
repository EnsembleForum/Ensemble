from typing import cast
from ..helpers import put, get
from ..consts import URL
from backend.types.auth import JWT
from backend.types.exam_mode import IExamModeInfo

URL = f"{URL}/admin/exam_mode"


def is_on(token: JWT) -> IExamModeInfo:
    """
    # GET `/admin/exam_mode/is_on`

    Get whether exam mode is on

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Returns
    * `is_on` (`bool`): Whether exam mode is on
    """
    return cast(
        IExamModeInfo,
        get(
            token,
            f"{URL}/is_on",
            {}
        ),
    )


def toggle_exam_mode(token: JWT) -> IExamModeInfo:
    """
    # PUT `/admin/exam_mode/toggle`

    Toggles whether exam mode is on

    ## Permissions
    * `SetExamMode`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Returns
    * `is_on` (`bool`): Whether exam mode is on
    """
    return cast(
        IExamModeInfo,
        put(
            token,
            f"{URL}/toggle",
            {}
        ),
    )
