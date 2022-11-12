"""
# Backend / Models / Analytics
"""
from piccolo.query.methods.select import Count
from typing import cast, Literal, Union
from backend.types.analytics import IAllStats, IAnalyticsValue, IGroupStats
from .user import User
from .tables import (TPost, TComment, TReply, TPostReacts,
                     TCommentReacts, TReplyReacts)


class Analytics:

    @classmethod
    def get_sorted_result(
        cls,
        unsorted: list[IAnalyticsValue],
        num: int
    ) -> list[IAnalyticsValue]:
        return sorted(
            unsorted,
            key=lambda x: (-x["count"], User(x["user_id"]).name_first)
        )[:num]

    @classmethod
    def num_posts(cls) -> int:
        """
        Returns the number of posts in the forum

        ### Returns:
        * int: number of posts in the forum
        """
        return cast(int, TPost.count().run_sync())

    @classmethod
    def num_comments(cls) -> int:
        """
        Returns the number of comments in the forum

        ### Returns:
        * int: number of comments in the forum
        """
        return cast(int, TComment.count().run_sync())

    @classmethod
    def num_replies(cls) -> int:
        """
        Returns the number of replies in the forum

        ### Returns:
        * int: number of replies in the forum
        """
        return cast(int, TReply.count().run_sync())

    @classmethod
    def top_creators(
        cls,
        table: type[Union[TPost, TComment, TReply]],
        group: list[Literal["Administrator", "Moderator", "User"]] = None,
        num: int = 10
    ) -> list["IAnalyticsValue"]:
        """
        Returns the top creators of posts/comments/replies
        Sorted from most to least number of posts/comments/replies,
        then by first name

        ### Args:
        * `table` (`type[Union[TPost, TComment, TReply]]`):
            Table to look for content in

        * `group` (`list[Literal["Administrator", "Moderator", "User"]]`):
            Search for top creators among the given Permission Groups

        * `num` (`int`): Max no. of users to return

        ### Returns:
        * `list[IAnalyticsValue]`:
            list of users and their post/comment/reply count
        """

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

        return cls.get_sorted_result(
            cast(list[IAnalyticsValue], result),
            num
        )

    @classmethod
    def top_me_too(
        cls,
        group: list[Literal["Administrator", "Moderator", "User"]] = None,
        num: int = 10
    ) -> list["IAnalyticsValue"]:
        """
        Returns the users who received the most number of me_too's
        Sorted from most to least number of me_too's, then by first name

        ### Args:

        * `group` (`list[Literal["Administrator", "Moderator", "User"]]`):
            Search for top creators among the given Permission Groups

        * `num` (`int`): Max no. of users to return

        ### Returns:
        * `list[IAnalyticsValue]`:
            list of users and the no. of me_too's they received
        """
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

        return cls.get_sorted_result(
            cast(list[IAnalyticsValue], result),
            num
        )

    @classmethod
    def top_thanks(
        cls,
        group: list[Literal["Administrator", "Moderator", "User"]] = None,
        num: int = 10
    ) -> list["IAnalyticsValue"]:
        """
        Returns the users who received the most number of thanks
        Sorted from most to least number of thanks, then by first name

        ### Args:

        * `group` (`list[Literal["Administrator", "Moderator", "User"]]`):
            Search for top creators among the given Permission Groups

        * `num` (`int`): Max no. of users to return

        ### Returns:
        * `list[IAnalyticsValue]`:
            list of users and the no. of thanks they received
        """
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

        while len(comments) > 0 and len(replies) > 0:
            if comments[0]["user_id"] < replies[0]["user_id"]:
                result.append(comments.pop(0))
            elif comments[0]["user_id"] > replies[0]["user_id"]:
                result.append(replies.pop(0))
            elif comments[0]["user_id"] == replies[0]["user_id"]:
                r = replies.pop(0)
                c = comments.pop(0)
                c["count"] += r["count"]
                result.append(c)

        if len(comments) > 0:
            result += comments
        if len(replies) > 0:
            result += replies

        return cls.get_sorted_result(
            cast(list[IAnalyticsValue], result),
            num
        )

    @classmethod
    def get_group_stats(
        cls,
        group: list[Literal["Administrator", "Moderator", "User"]] = None
    ) -> IGroupStats:
        """
        Returns the forum stats for users among the given Permission Group

        ### Args:
        * `group` (`list[Literal["Administrator", "Moderator", "User"]]`):
            Search for top creators among the given Permission Groups

        * `num` (`int`): Max no. of users to return

        ### Returns:
        * `IGroupStats`: Dictionary containing forum stats of top users
        """
        if group:
            return {
                "top_posters": cls.top_creators(TPost, group),
                "top_commenters": cls.top_creators(TComment, group),
                "top_repliers": cls.top_creators(TReply, group),
                "top_me_too": cls.top_me_too(group),
                "top_thanks": cls.top_thanks(group),
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
    def all_stats(cls) -> IAllStats:
        """
        Returns the full forum analytics

        ### Returns:
        * `IAllStats`: Dictionary containing full forum analytics
        """
        return {
            "total_posts": cls.num_posts(),
            "total_comments": cls.num_comments(),
            "total_replies": cls.num_replies(),
            "all_users": cls.get_group_stats(),
            "students": cls.get_group_stats(["User"]),
            "staff": cls.get_group_stats(["Administrator", "Moderator"]),
        }
