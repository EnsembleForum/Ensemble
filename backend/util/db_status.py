"""
# Backend / Util / DB Status

Tools for checking on the database status
"""
from piccolo.table import drop_db_tables_sync, create_db_tables_sync
from backend.models import tables

# List of tables to clear
ALL_TABLES: list[type[tables._BaseTable]] = [
    tables.TAuthConfig,
    tables.TUser,
    tables.TPermissionGroup,
    tables.TPermissionUser,
    tables.TToken,
]


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
