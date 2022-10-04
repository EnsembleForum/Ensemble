"""
# Backend / Models / Tables

Contains the definitions for tables used within the database
"""

from piccolo.table import Table
from piccolo.columns import Integer, Array, ForeignKey


class PresetPermissions(Table):
    """
    Table containing preset permission definitions.
    """
    allowed = Array(Integer())
    disallowed = Array(Integer())


class Permissions(Table):
    """
    Table containing all permission sets available.
    """
    allowed = Array(Integer())
    disallowed = Array(Integer())
    inherits_from = ForeignKey(PresetPermissions)
