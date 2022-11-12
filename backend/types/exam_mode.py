from typing import TypedDict


class IExamModeInfo(TypedDict):
    """
    Whether exam mode is enabled or not
    
    * `is_enabled`: `bool`
    """
    is_enabled: bool
