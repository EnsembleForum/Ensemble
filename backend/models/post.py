"""
# Backend / Models / Post
"""
from .tables import TComment, TPost, TPostReacts, TPostTags, TReport
from .user import User
from .tag import Tag
from .comment import Comment
from .post_queue import Queue
from .permissions import Permission
from backend.util.db_queries import get_by_id, assert_id_exists
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import PostId, CommentId
from backend.types.post import IPostBasicInfo, IPostFullInfo
from typing import cast
from datetime import datetime
from fuzzywuzzy import fuzz  # type: ignore


class Post:
    """
    Represents a post of Ensemble
    """

    def __init__(self, id: PostId):
        """
        Create a post object shadowing an existing in the database

        ### Args:
        * `id` (`int`): post id

        ### Raises:
        * `IdNotFound`: post does not exist
        """
        assert_id_exists(TPost, id, "Post")
        self.__id = id

    @classmethod
    def create(
        cls,
        author: User,
        heading: str,
        text: str,
        tags: list[Tag],
        private: bool = False,
        anonymous: bool = False,
    ) -> "Post":
        """
        Create a new post

        ### Args:
        * `author` (`int`): user id of author

        * `heading` (`str`): heading of post

        * `text` (`str`): contents of post

        * `tags` (`list[int]`): tags attached to post

        ### Returns:
        * `Post`: the post object
        """
        assert_valid_str_field(heading, "heading")
        assert_valid_str_field(text, "post")
        val = (
            TPost(
                {
                    TPost.author: author.id,
                    TPost.heading: heading,
                    TPost.text: text,
                    TPost.timestamp: datetime.now(),
                    TPost.queue: Queue.get_main_queue().id,
                    TPost.private: private,
                    TPost.anonymous: anonymous,
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(PostId, val["id"])
        p = Post(id)
        for t in tags:
            TPostTags(
                {
                    TPostTags.post: id,
                    TPostTags.tag: t.id,
                }
            ).save().run_sync()
        return p

    @classmethod
    def all(cls) -> list["Post"]:
        """
        Returns a list of all posts
        in order of newest to oldest
        ### Returns:
        * `list[Post]`: list of posts
        """
        return [
            Post(p["id"]) for p in
            TPost.select().order_by(TPost.id, ascending=False).run_sync()
        ]

    def can_view(self, user: User) -> bool:
        """
        Returns whether the user can view this post
        ### Returns:
        * `bool`: whether the user can view the post
        """
        if (self.private or self.closed or self.deleted)\
                and self.author != user:
            return user.permissions.can(Permission.ViewPrivate)
        return True

    @classmethod
    def can_view_list(cls, user: User) -> list["Post"]:
        """
        Returns a list of posts that the given user has permissions to view
        ### Returns:
        * `list[Post]`: list of posts
        """
        permitted_list = [p for p in cls.all() if p.can_view(user)]

        return permitted_list

    @classmethod
    def search_posts(cls, user: User, search_term: str) -> list["Post"]:
        """
        Returns a list of posts that match the search term
        ### Returns:
        * `list[Post]`: list of posts
        """
        def sim_score(post: Post, search_term: str):
            return (
                fuzz.partial_ratio(post.heading, search_term) +
                fuzz.partial_ratio(post.text, search_term)
            ) / 2

        matches = []
        min_score = 35
        for p in cls.can_view_list(user):
            score = sim_score(p, search_term)
            if score >= min_score:  # Filter out terrible matches
                matches.append((p, score))
        matches = sorted(matches, key=lambda x: (-x[1], -x[0].id))
        return [p for p, _ in matches]

    @property
    def comments(self) -> list["Comment"]:
        """
        Returns a list of all comments belonging to the post
        Comments are sorted by marked as accepted, thanks then newest to oldest
        ### Returns:
        * `list[Comment]`: list of comments
        """
        comments = [
            Comment(c["id"])
            for c in TComment.select()
            .where(TComment.parent == self.__id)
            .order_by(TComment.id)
            .run_sync()
        ]

        return sorted(
            comments,
            key=lambda x: (not x.accepted, -x.thanks, x.id)
        )

    def delete(self):
        """
        Mark this post as deleted
        """
        self.queue = Queue.get_deleted_queue()

    @property
    def deleted(self) -> bool:
        """
        Whether this post is deleted or not
        """
        return self.queue == Queue.get_deleted_queue()

    def _get(self) -> TPost:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TPost, self.__id)

    @property
    def id(self) -> PostId:
        """
        Identifier of the post
        """
        return self.__id

    @property
    def heading(self) -> str:
        """
        The heading of the post
        """
        return self._get().heading

    @heading.setter
    def heading(self, new_heading: str):
        assert_valid_str_field(new_heading, "new heading")
        row = self._get()
        row.heading = new_heading
        row.save().run_sync()

    @property
    def answered(self) -> Comment | None:
        """
        Returns the comment that is marked as accepted
        """
        ans = self._get().answered
        if not ans:
            return None
        else:
            return Comment(CommentId(ans))

    @answered.setter
    def answered(self, comment: Comment | None):
        """
        Sets whether the post is answered
        """
        row = self._get()
        if comment is not None:
            row.answered = comment.id
        else:
            row.answered = None
        row.save().run_sync()

    @property
    def text(self) -> str:
        """
        The text of the post
        """
        return self._get().text

    @text.setter
    def text(self, new_text: str):
        assert_valid_str_field(new_text, "post")
        row = self._get()
        row.text = new_text
        row.save().run_sync()

    @property
    def author(self) -> "User":
        """
        Returns a reference to the user that owns this token

        ### Returns:
        * `User`: user
        """
        return User(self._get().author)

    @property
    def queue(self) -> "Queue":
        """
        Returns a reference to the queue that the post belongs in

        ### Returns:
        * `Queue`: Queue that has the post
        """
        return Queue(self._get().queue)

    @queue.setter
    def queue(self, new_queue: "Queue"):
        row = self._get()
        row.queue = new_queue.id
        row.save().run_sync()

    @property
    def tags(self) -> list[Tag]:
        """
        Returns a list of tags attached to the post
        sorted in alphabetical order

        ### Returns:

        * list[Tag]: list of tags
        """
        tags = [
            Tag(t["tag"])
            for t in
            TPostTags.select().where(
                TPostTags.post == self.id
            ).run_sync()
        ]
        return sorted(tags, key=lambda x: x.name)

    @tags.setter
    def tags(self, new_tags: list[Tag]):
        TPostTags.delete().where(TPostTags.post == self.id).run_sync()
        for t in new_tags:
            TPostTags(
                {
                    TPostTags.post: self.id,
                    TPostTags.tag: t.id,
                }
            ).save().run_sync()

    @property
    def me_too(self) -> int:
        """
        Returns the number of 'me too' reacts

        ### Returns:
        * int: number of 'me too' reacts
        """
        return cast(
            int,
            TPostReacts.count().where(TPostReacts.post == self.id).run_sync()
        )

    def has_reacted(self, user: User) -> bool:
        """
        Returns whether the user has reacted to this post
        """
        return cast(
            bool,
            TPostReacts.exists()
            .where(TPostReacts.post == self.id,
                   TPostReacts.user == user.id).run_sync()
        )

    def react(self, user: User):
        """
        React to the post if the user has not reacted to the post
        Unreact to the post if the user has reacted to the post

        ### Args:
        * `user` (`User`): User reacting/un-reacting to the post
        """
        if not self.has_reacted(user):
            TPostReacts(
                {
                    TPostReacts.user: user.id,
                    TPostReacts.post: self.id,
                }
            ).save().run_sync()
        else:
            TPostReacts.delete().where(TPostReacts.user == user.id,
                                       TPostReacts.post == self.id).run_sync()

    @property
    def timestamp(self) -> datetime:
        """
        Returns the timestamp of when the post was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

    @property
    def private(self) -> bool:
        """
        Returns true if the post is a private post

        ### Returns:
        * bool: private
        """
        return self._get().private

    @private.setter
    def private(self, new_private: bool):
        row = self._get()
        row.private = new_private
        row.save().run_sync()

    @property
    def anonymous(self) -> bool:
        """
        Returns true if the post is an anonymous post

        ### Returns:
        * bool: anonymous
        """
        return self._get().anonymous

    @anonymous.setter
    def anonymous(self, new_anonymous: bool):
        row = self._get()
        row.anonymous = new_anonymous
        row.save().run_sync()

    @property
    def closed(self) -> bool:
        """
        Returns true if this post was closed by a mod/admin

        ### Returns:
        * bool: closed
        """
        return self.queue == Queue.get_closed_queue()

    def closed_toggle(self):
        """
        Close post if it was not
        Un-close post if it was
        """
        if self.closed:
            if self.answered:
                self.queue = Queue.get_answered_queue()
            else:
                self.queue = Queue.get_main_queue()
        else:
            self.queue = Queue.get_closed_queue()

    def can_view_op(self, user: User) -> bool:
        """
        Returns whether the given user should be able to view who made this
        post.
        """
        if self.author == user:
            return True
        if self.anonymous:
            return user.permissions.can(Permission.ViewAnonymousOP)
        else:
            return True

    def report(self, user: User):
        """
        Toggle whether the given user has reported the post
        """
        if self.user_reported(user):
            TReport.delete().where(
                TReport.user == user.id
                & TReport.post == self.id
            ).run_sync()
        else:
            TReport(user=user.id, post=self.id).save().run_sync()

    def unreport(self):
        """
        Remove all reports of this post
        """
        TReport.delete().where(TReport.post == self.id).run_sync()

    def user_reported(self, user: User) -> bool:
        """
        Returns whether this user has reported the post
        """
        return TReport.exists().where(
            TReport.user == user.id
            & TReport.post == self.id
        ).run_sync()

    def report_count(self, user: User) -> int:
        """
        Returns the report count, or zero if the given user doesn't have
        permission to view reports
        """
        if not user.permissions.can(Permission.ViewReports):
            return 0
        else:
            return TReport.count().where(
                TReport.post.id == self.id
            ).run_sync()

    def basic_info(self, user: User) -> IPostBasicInfo:
        """
        Returns the basic info of a post

        ### Returns:
        * IPostBasicInfo: Dictionary containing basic info a post
        """
        return {
            "author": self.author.id if self.can_view_op(user) else None,
            "heading": self.heading,
            "post_id": PostId(self.id),
            "tags": [t.id for t in self.tags],
            "me_too": self.me_too,
            "private": self.private,
            "closed": self.closed,
            "deleted": self.deleted,
            "reported": self.report_count(user) > 0,
            "anonymous": self.anonymous,
            "answered": self.answered is not None,
        }

    def full_info(self, user: User) -> IPostFullInfo:
        """
        Returns the full info of a post

        ### Returns:
        * IPostFullInfo: Dictionary containing full info a post
        """
        return {
            "post_id": self.id,
            "author": self.author.id if self.can_view_op(user) else None,
            "heading": self.heading,
            "tags": [t.id for t in self.tags],
            "me_too": self.me_too,
            "text": self.text,
            "timestamp": int(self.timestamp.timestamp()),
            "comments": [c.id for c in self.comments],
            "private": self.private,
            "anonymous": self.anonymous,
            "closed": self.closed,
            "deleted": self.deleted,
            "report_count": self.report_count(user),
            "user_reported": self.user_reported(user),
            "user_reacted": self.has_reacted(user),
            "answered": self.answered.id if self.answered else None,
            "queue": self.queue.name
        }
