"""
# Backend / Models / Analytics
"""
from piccolo.query.methods.select import Count
from typing import cast

# from backend.util import http_errors
from backend.types.analytics import IAllStats, IAnalyticsValue
from .user import User
from .tables import (TPost, TComment, TReply)


class Analytics:

    @classmethod
    def num_posts(cls) -> int:
        return cast(int, TPost.count().run_sync())

    @classmethod
    def num_comments(cls) -> int:
        return cast(int, TComment.count().run_sync())

    @classmethod
    def num_replies(cls) -> int:
        return cast(int, TReply.count().run_sync())

    @classmethod
    def top_posters(cls, num=10, group=None) -> list["IAnalyticsValue"]:
        if group:
            result = TPost.select(
                TPost.author.as_alias("user_id"),
                Count(TPost.author).as_alias("count")
            ).where(
                TPost.author.permissions.parent.name == group  # type: ignore
            ).group_by(
                TPost.author
            ).run_sync()
        else:
            result = TPost.select(
                TPost.author.as_alias("user_id"),
                Count(TPost.author).as_alias("count")
            ).group_by(
                TPost.author
            ).run_sync()

        return sorted(
            cast(list[IAnalyticsValue], result),
            key=lambda x: x["count"]
        )
    
    @classmethod
    def all_stats(cls, user: User) -> IAllStats:
        return {
            "total_posts": cls.num_posts(),
            "total_comments": cls.num_comments(),
            "total_replies": cls.num_replies(),
            "top_posters": cls.top_posters()
        }
        
