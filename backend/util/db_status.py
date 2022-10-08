"""
# Backend / Util / DB Status

Tools for checking on the database status
"""
from backend.models import tables

# List of tables to clear
ALL_TABLES: list[type[tables._BaseTable]] = [
    tables.TUser,
    tables.TPermissionGroup,
    tables.TPermissionUser,
]


def clear_all():
    """
    Clear the entire database

    WARNING: This literally deletes everything
    """
    # Make sure they all exist beforehand
    init()
    for t in ALL_TABLES:
        t.delete(force=True).run_sync()


def init():
    """
    Initialise the database

    This does nothing if the database is already initialised, meaning it is
    safe to call during startup.
    """
    for t in ALL_TABLES:
        t.create_table(if_not_exists=True).run_sync()
