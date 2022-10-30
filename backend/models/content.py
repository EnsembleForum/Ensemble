from abc import ABC, abstractproperty
from typing import Literal
from backend.models.tables import _BaseTable
from backend.types.identifiers import Identifier
from backend.util.db_queries import assert_id_exists


class Content(ABC):
    def __init__(
        self,
        table: type[_BaseTable],
        id: Identifier,
        content_type: Literal["post", "comment", "reply"]
    ):
        self.__id = id
        self.table = table
        self.content_type = content_type
        assert_id_exists(table, id, content_type)

    @abstractproperty
    def id(self) -> Identifier:
        """
        Identifier of the post
        """
        return self.__id

    def delete(self):
        self.table.delete().where(self.table.id == self.id).run_sync()
