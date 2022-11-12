from typing import cast
from ..helpers import put, get
from ..consts import URL
from backend.types.auth import JWT
from backend.types.exam_mode import IExamModeInfo

URL = f"{URL}/admin/exam_mode"


def exam_is_enabled(token: JWT) -> IExamModeInfo:
    """
    # GET `/admin/exam_mode/is_enabled`

    Get whether exam mode is on

    ## Permissions
    * `PostView`

    ## Header
    * `Authorization` (`str`): JWT of the user

    ## Returns
    Object containing
    * `is_enabled` (`bool`): Whether exam mode is enabled
    """
    return cast(
        IExamModeInfo,
        get(
            token,
            f"{URL}/is_enabled",
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
    Object containing
    * `is_enabled` (`bool`): Whether exam mode is on
    """
    return cast(
        IExamModeInfo,
        put(
            token,
            f"{URL}/toggle",
            {}
        ),
    )
