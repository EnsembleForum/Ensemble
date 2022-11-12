from typing import TypedDict
from .identifiers import UserId


class IAnalyticsValue(TypedDict):
    user_id: UserId
    count: int


class IGroupStats(TypedDict):
    top_posters: list[IAnalyticsValue]
    top_commenters: list[IAnalyticsValue]
    top_repliers: list[IAnalyticsValue]


class IAllStats(TypedDict):
    total_posts: int
    total_comments: int
    total_replies: int
    all_users: IGroupStats
    students: IGroupStats
    staff: IGroupStats
