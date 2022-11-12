from typing import TypedDict
from .identifiers import UserId


class IAnalyticsValue(TypedDict):
    """
    Statistic for a user

    * `user_id`: `UserId`
    * `count`: `int`
    """
    user_id: UserId
    count: int


class IGroupStats(TypedDict):
    """
    Top users among a Permission Group

    * `top_posters`: `list[IAnalyticsValue]`
    * `top_commenters`: `list[IAnalyticsValue]`
    * `top_repliers`: `list[IAnalyticsValue]`
    * `top_me_too`: `list[IAnalyticsValue]`
    * `top_thanks`: `list[IAnalyticsValue]`
    """
    top_posters: list[IAnalyticsValue]
    top_commenters: list[IAnalyticsValue]
    top_repliers: list[IAnalyticsValue]
    top_me_too: list[IAnalyticsValue]
    top_thanks: list[IAnalyticsValue]


class IAllStats(TypedDict):
    """
    Full analytics for the forum

    * `total_posts`: `int`
    * `total_comments`: `int`
    * `total_replies`: `int`
    * `all_users`: `IGroupStats`
    * `students`: `IGroupStats`
    * `staff`: `IGroupStats`
    """
    total_posts: int
    total_comments: int
    total_replies: int
    all_users: IGroupStats
    students: IGroupStats
    staff: IGroupStats
