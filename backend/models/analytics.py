"""
# Backend / Models / Analytics
"""
from piccolo.query.methods.select import Count
from typing import cast, Literal, Union

# from backend.util import http_errors
from backend.types.analytics import IAllStats, IAnalyticsValue, IGroupStats
from .user import User
from .tables import (TPost, TComment, TReply, TPostReacts,
                     TCommentReacts, TReplyReacts)


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
        group: list[Literal["Administrator", "Moderator", "User"]] = None,
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
            key=lambda x: (-x["count"], User(x["user_id"]).name_first)
        )[:num]

    @classmethod
    def get_group_stats(
        cls,
        group: list[Literal["Administrator", "Moderator", "User"]] = None
    ) -> IGroupStats:
        if group:
            return {
                "top_posters": cls.top_creators(TPost, group),
                "top_commenters": cls.top_creators(TComment, group),
                "top_repliers": cls.top_creators(TReply, group),
                "top_me_too": cls.top_me_too(group),
                "top_thanks": cls.top_thanks(),
            }
        else:
            return {
                "top_posters": cls.top_creators(TPost),
                "top_commenters": cls.top_creators(TComment),
                "top_repliers": cls.top_creators(TReply),
                "top_me_too": cls.top_me_too(),
                "top_thanks": cls.top_thanks()
            }

    @classmethod
    def top_me_too(
        cls,
        group: list[Literal["Administrator", "Moderator", "User"]] = None,
        num: int = 10
    ) -> list["IAnalyticsValue"]:
        if group:
            result = TPostReacts.select(
                TPostReacts.post.author.as_alias("user_id"),
                Count().as_alias("count")
            ).where(
                TPostReacts.post.author.permissions.  # type: ignore
                parent.name.is_in(group)
            ).group_by(
                TPostReacts.post.author
            ).run_sync()
        else:
            result = TPostReacts.select(
                TPostReacts.post.author.as_alias("user_id"),
                Count().as_alias("count")
            ).group_by(
                TPostReacts.post.author
            ).run_sync()

        return sorted(
            cast(list[IAnalyticsValue], result),
            key=lambda x: (-x["count"], User(x["user_id"]).name_first)
        )[:num]

    @classmethod
    def top_thanks(
        cls,
        group: list[Literal["Administrator", "Moderator", "User"]] = None,
        num: int = 10
    ) -> list["IAnalyticsValue"]:

        if group:
            comments = TCommentReacts.select(
                TCommentReacts.comment.author.as_alias(
                    "user_id"),  # type: ignore
                Count().as_alias("count")
            ).where(
                TCommentReacts.comment.author.permissions.  # type: ignore
                parent.name.is_in(group)
            ).group_by(
                TCommentReacts.comment.author
            ).order_by(
                TCommentReacts.comment.author
            ).run_sync()

            replies = TReplyReacts.select(
                TReplyReacts.reply.author.as_alias("user_id"),  # type: ignore
                Count().as_alias("count")
            ).where(
                TReplyReacts.reply.author.permissions.  # type: ignore
                parent.name.is_in(group)
            ).group_by(
                TReplyReacts.reply.author
            ).order_by(
                TReplyReacts.reply.author
            ).run_sync()
        else:
            comments = TCommentReacts.select(
                TCommentReacts.comment.author.as_alias(
                    "user_id"),  # type: ignore
                Count().as_alias("count")
            ).group_by(
                TCommentReacts.comment.author
            ).order_by(
                TCommentReacts.comment.author
            ).run_sync()

            replies = TReplyReacts.select(
                TReplyReacts.reply.author.as_alias("user_id"),  # type: ignore
                Count().as_alias("count")
            ).group_by(
                TReplyReacts.reply.author
            ).order_by(
                TReplyReacts.reply.author
            ).run_sync()

        result = []

        for c in comments:
            if len(replies) == 0:
                break
            r = replies.pop(0)
            if c["user_id"] == r["user_id"]:
                c["count"] += r["count"]
            else:
                result.append(r)

        result += comments

        return sorted(
            cast(list[IAnalyticsValue], result),
            key=lambda x: (-x["count"], User(x["user_id"]).name_first)
        )[:num]

    @classmethod
    def all_stats(cls, user: User) -> IAllStats:
        return {
            "total_posts": cls.num_posts(),
            "total_comments": cls.num_comments(),
            "total_replies": cls.num_replies(),
            "all_users": cls.get_group_stats(),
            "students": cls.get_group_stats(["User"]),
            "staff": cls.get_group_stats(["Administrator", "Moderator"]),
        }
