"""
# Backend / Models / Analytics
"""
from piccolo.query.methods.select import Count
from typing import cast, Literal, Union

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
    def top_creators(
        cls,
        table: type[Union[TPost, TComment, TReply]],
        group: list[Literal["Administrator", "Moderator", "Student"]] = None,
        num: int = 10
    ) -> list["IAnalyticsValue"]:
        if group:
            result = table.select(
                table.author.as_alias("user_id"),
                Count(table.author).as_alias("count")
            ).where(
                table.author.permissions.
                parent.name.is_in(group)  # type: ignore
            ).group_by(
                table.author
            ).run_sync()
        else:
            result = table.select(
                table.author.as_alias("user_id"),
                Count(table.author).as_alias("count")
            ).group_by(
                table.author
            ).run_sync()

        return sorted(
            cast(list[IAnalyticsValue], result),
            key=lambda x: x["count"]
        )[:num]

    @classmethod
    def all_stats(cls, user: User) -> IAllStats:
        return {
            "total_posts": cls.num_posts(),
            "total_comments": cls.num_comments(),
            "total_replies": cls.num_replies(),
            "students": {
                "top_posters": cls.top_creators(TPost, ["Student"]),
                "top_commenters": cls.top_creators(TComment, ["Student"]),
                "top_repliers": cls.top_creators(TReply, ["Student"])
            },
            "staff": {
                "top_posters": cls.top_creators(
                    TPost,
                    ["Administrator", "Moderator"]
                ),
                "top_commenters": cls.top_creators(
                    TComment,
                    ["Administrator", "Moderator"]
                ),
                "top_repliers": cls.top_creators(
                    TReply,
                    ["Administrator", "Moderator"]
                )
            }
        }
