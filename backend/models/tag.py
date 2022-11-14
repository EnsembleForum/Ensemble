from .tables import TComment, TPost, TTag, TPostTags
from .user import User
from .post import Post
from .comment import Comment
from .queue import Queue
from .permissions import Permission
from backend.util.db_queries import get_by_id, assert_id_exists
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import PostId, CommentId, TagId
from backend.types.post import IPostBasicInfo, IPostFullInfo
from typing import cast  # , TYPE_CHECKING
from datetime import datetime
# if TYPE_CHECKING:
#     from backend.models.queue import Queue


class Tag:
    """
    Represents a post of Ensemble
    """

    def __init__(self, id: TagId):
        """
        Create a post object shadowing an existing in the database

        ### Args:
        * `id` (`int`): post id

        ### Raises:
        * `IdNotFound`: post does not exist
        """
        assert_id_exists(TTag, id, "TTag")
        self.__id = id

    @classmethod
    def create(
        cls,
        name: str,
    ) -> "Tag":
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
        assert_valid_str_field(name, "name")
        val = (
            TTag(
                {
                    TTag.name: name,
                }
            )
            .save()
            .run_sync()[0]
        )
        id = cast(TagId, val["id"])
        return Tag(id)

    @classmethod
    def all(cls) -> list["Tag"]:
        """
        Returns a list of all tags
        in order of newest to oldest
        ### Returns:
        * `list[Tag]`: list of tags
        """
        return [
            Tag(p["id"]) for p in
            TTag.select().order_by(TTag.id, ascending=False).run_sync()
        ]
    def _get(self) -> TTag:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TTag, self.__id)

    @property
    def id(self) -> TagId:
        return self.__id

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, new_name):
        assert_valid_str_field(new_name, "new name")
        row = self._get()
        row.name = new_name
        row.save().run_sync()
