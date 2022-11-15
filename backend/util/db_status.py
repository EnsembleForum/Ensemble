"""
# Backend / Util / DB Status

Tools for checking on the database status
"""
from piccolo.table import drop_db_tables_sync, create_db_tables_sync
from backend.models import tables


def get_all_tables() -> list[type[tables._BaseTable]]:
    """Return a list of all subclasses of _BaseTable"""
    t_strs = filter(
        lambda t: t.startswith("T"),
        dir(tables),
    )
    t_objects = map(
        # https://github.com/python/mypy/issues/9656
        lambda t: getattr(tables, t),  # type: ignore
        t_strs,
    )
    t_subclasses = filter(
        lambda t: isinstance(t, type) and issubclass(t, tables._BaseTable),
        t_objects,
    )
    return list(t_subclasses)


# List of tables to clear
ALL_TABLES = get_all_tables()


def clear_all():
    """
    Clear the entire database

    WARNING: This literally deletes everything
    """
    # Make sure they all exist beforehand
    init()
    drop_db_tables_sync(*ALL_TABLES)
    # Then recreate them
    init()


def init():
    """
    Initialise the database

    This does nothing if the database is already initialised, meaning it is
    safe to call during startup.
    """
    create_db_tables_sync(*ALL_TABLES, if_not_exists=True)
