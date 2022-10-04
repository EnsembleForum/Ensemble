"""
# Backend / Models / Tables

Contains the definitions for tables used within the database.

All tables should begin with T to distinguish them from their model classes.
"""

from piccolo.table import Table
from piccolo.columns import Serial, Text, Integer, Array, ForeignKey


class _BaseTable(Table):
    id = Serial(primary_key=True)


class TPermissionPreset(_BaseTable):
    """
    Table containing preset permission definitions.
    """
    name = Text()
    allowed = Array(Integer())
    disallowed = Array(Integer())


class TPermissionUser(_BaseTable):
    """
    Table containing all permission sets available.
    """
    allowed = Array(Integer())
    disallowed = Array(Integer())
    parent = ForeignKey(TPermissionPreset)
    user = ForeignKey('TUser')


class TUser(_BaseTable):
    """
    Table containing all user data
    """
    name_first = Text()
    name_last = Text()
    permissions = ForeignKey(TPermissionUser)
