from typing import TypedDict
from .identifiers import UserId


class IAnalyticsValue(TypedDict):
    user_id: UserId
    count: int


class IAllStats(TypedDict):
    total_posts: int
    total_comments: int
    total_replies: int
    top_posters: list[IAnalyticsValue]
