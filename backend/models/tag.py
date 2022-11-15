from .tables import TTag, TPostTags
from backend.types.tag import ITagBasicInfo
from backend.util.db_queries import get_by_id, assert_id_exists
from backend.util.validators import assert_valid_str_field
from backend.types.identifiers import TagId
from typing import cast


class Tag:
    """
    Represents a post of Ensemble
    """

    def __init__(self, id: TagId):
        """
        Create a post object shadowing an existing in the database

        ### Args:
        * `id` (`TagId`): Tag id

        """
        assert_id_exists(TTag, id, "TTag")
        self.__id = id

    @classmethod
    def create(
        cls,
        name: str,
    ) -> "Tag":
        """
        Create a new tag

        ### Args:
        * `name` (`str`): name

        ### Returns:
        * `Tag`: the Tag object
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
        return self._get().name

    @name.setter
    def name(self, new_name):
        assert_valid_str_field(new_name, "new name")
        row = self._get()
        row.name = new_name
        row.save().run_sync()

    def delete(self):
        """
        Deletes this tag from the database

        """
        TPostTags.delete().where(TPostTags.id == self.id).run_sync()

    def basic_info(self) -> ITagBasicInfo:
        """
        Returns the basic info of a post

        ### Returns:
        * IPostBasicInfo: Dictionary containing basic info a post
        """
        return {
            "tag_id": self.id,
            "name": self.name,
        }
