"""
# Backend / Util / Db Queries

Contains helper code for running database queries
"""
from backend.models.tables import _BaseTable
from typing import TypeVar, cast
from .exceptions import IdNotFound


T = TypeVar('T', bound=_BaseTable)


def id_exists(table: type[_BaseTable], id: int) -> bool:
    """
    Returns whether an ID exists in the given table of the database

    ### Args:
    * `table` (`type[T]`): table to search in

    * `id` (`int`): ID to search for

    ### Returns:
    * `bool`:
    """
    if not isinstance(id, int):
        raise TypeError(
            f"ID {id!r} is a {type(id).__name__}, but should be an int - this "
            f"probably means you're not getting database values correctly"
        )
    return cast(bool, table.exists().where(table.id == id).run_sync())


def assert_id_exists(table: type[_BaseTable], id: int, type: str = "") -> None:
    """
    Raises a BadRequest if a given ID is not present

    ### Args:
    * `table` (`type[_BaseTable]`): table to search

    * `id` (`int`): id to search for
    """
    if not id_exists(table, id):
        raise IdNotFound(f"{type}Id {id} not found")


def get_by_id(table: type[T], id: int) -> T:
    """
    Returns a row in the table that has the given ID

    This row can be edited as required, as long as it is saved afterwards.

    ### Args:
    * `table` (`type[T]`): table to search in

    * `id` (`int`): id to search for

    ### Returns:
    * `T`: value to search for

    ### Raises:
    * `KeyError`: when the value doesn't exist
    """
    result = table.objects().where(table.id == id).first().run_sync()
    if result is None:
        raise IdNotFound(f"id {id} not found in table {table.__name__}")
    return cast(T, result)
