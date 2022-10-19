"""
# Backend / Models / Post
"""
from .tables import TComment, TPost
from .user import User
from .comment import Comment
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import PostId
from backend.types.post import IPostBasicInfo, IPostFullInfo, IReacts
from typing import cast
from datetime import datetime


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
        tags: list[int],
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
                    TPost.me_too: 0,
                    TPost.thanks: 0,
                    TPost.tags: tags,
                    TPost.timestamp: datetime.now()
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(PostId, val["id"])
        return Post(id)

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

    @property
    def comments(self) -> list["Comment"]:
        """
        Returns a list of all comments belonging to the post
        TODO Should this be ordered from newest to oldest?
        ### Returns:
        * `list[Comment]`: list of comments
        """
        return [
            Comment(c["id"])
            for c in TComment.select()
            .where(TComment.parent == self.__id)
            .order_by(TComment.id, ascending=False)
            .run_sync()
        ]

    @classmethod
    def delete(cls, post_id: PostId) -> PostId:
        """
        Deletes a post from the database

        ### Returns:
        * `PostId`: identifier of the deleted post
        """
        TPost.delete().where(TPost.id == post_id).run_sync()
        return post_id

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
    def tags(self) -> list[int]:
        """
        Returns a list of tags attached to the post

        ### Returns:
        * list[int]: list of tags

        TODO: Need to define a new tag type, not used in sprint 1
        """
        return self._get().tags

    @tags.setter
    def tags(self, new_tags: list[int]):
        """
        TODO: Need to define a new tag type, not used in sprint 1
        """
        row = self._get()
        row.tags = new_tags
        row.save().run_sync()

    @property
    def me_too(self) -> int:
        """
        Returns the number of 'me too' reacts

        ### Returns:
        * int: number of 'me too' reacts
        """
        return self._get().me_too

    def me_too_inc(self):
        row = self._get()
        row.me_too += 1
        row.save().run_sync()

    def me_too_dec(self):
        row = self._get()
        row.me_too -= 1
        row.save().run_sync()

    @property
    def thanks(self) -> int:
        """
        Returns the number of 'thanks' reacts

        ### Returns:
        * int: number of 'thanks' reacts
        """
        return self._get().thanks

    def thanks_inc(self):
        row = self._get()
        row.thanks += 1
        row.save().run_sync()

    def thanks_dec(self):
        row = self._get()
        row.thanks -= 1
        row.save().run_sync()

    @property
    def timestamp(self) -> datetime:
        """
        Returns the timestamp of when the post was created

        ### Returns:
        * int: timestamp
        """
        return self._get().timestamp

    @property
    def reacts(self) -> IReacts:
        """
        Returns the reactions to the post

        ### Returns:
        * IReacts: Dictionary containing the reactions
        """
        return {
            "thanks": self.thanks,
            "me_too": self.me_too,
        }

    @property
    def basic_info(self) -> IPostBasicInfo:
        """
        Returns the basic info of a post

        ### Returns:
        * IPostBasicInfo: Dictionary containing basic info a post
        """
        return {
            "author": self.author.id,
            "heading": self.heading,
            "post_id": self.id,
            "tags": self.tags,
            "reacts": self.reacts,
        }

    @property
    def full_info(self) -> IPostFullInfo:
        """
        Returns the full info of a post

        ### Returns:
        * IPostFullInfo: Dictionary containing full info a post
        """
        return {
            "author": self.author.id,
            "heading": self.heading,
            "tags": self.tags,
            "reacts": self.reacts,
            "text": self.text,
            "timestamp": int(self.timestamp.timestamp()),
            "comments": [c.id for c in self.comments],
        }
