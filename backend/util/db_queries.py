"""
# Backend / Util / Db Queries

Contains helper code for running database queries
"""
from backend.models.tables import _BaseTable
from typing import TypeVar, cast


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
    return cast(bool, table.exists().where(table.id == id).run_sync())


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
        raise KeyError(f"id {id} not found in table {table}")
    return cast(T, result)
