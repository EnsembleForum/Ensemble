"""
# Backend / Models / Tables

Contains the definitions for tables used within the database.

All tables should begin with T to distinguish them from their model classes.
"""

from piccolo.table import Table
from piccolo.columns import (
    Serial,
    Text,
    Integer,
    Array,
    ForeignKey,
    Timestamp,
    Boolean,
)


class _BaseTable(Table):
    id = Serial(primary_key=True)


class TAuthConfig(_BaseTable):
    """
    Table containing a single row which is the server's auth config
    """

    address = Text()
    request_type = Text()
    username_param = Text()
    password_param = Text()
    success_regex = Text()


class TPermissionGroup(_BaseTable):
    """
    Table containing preset permission definitions.
    """

    name = Text()
    allowed = Array(Integer())
    disallowed = Array(Integer())
    immutable = Boolean()


class TPermissionUser(_BaseTable):
    """
    Table containing all permission sets available.
    """

    allowed = Array(Integer())
    disallowed = Array(Integer())
    parent = ForeignKey(TPermissionGroup)


class TUser(_BaseTable):
    """
    Table containing all user data
    """

    username = Text()
    name_first = Text()
    name_last = Text()
    email = Text()
    permissions = ForeignKey(TPermissionUser)


class TQueue(_BaseTable):
    immutable = Boolean()
    name = Text()


class TPost(_BaseTable):
    """
    Table containing all posts
    """

    author = ForeignKey(TUser)
    heading = Text()
    text = Text()
    tags = Array(Integer())
    me_too = Integer()
    thanks = Integer()
    timestamp = Timestamp()
    queue = ForeignKey(TQueue)


class TComment(_BaseTable):
    """
    Table containing all comments
    """

    author = ForeignKey(TUser)
    parent = ForeignKey(TPost)
    text = Text()
    me_too = Integer()
    thanks = Integer()
    timestamp = Timestamp()


class TReply(_BaseTable):
    """
    Table containing all replies
    """

    author = ForeignKey(TUser)
    parent = ForeignKey(TComment)
    text = Text()
    me_too = Integer()
    thanks = Integer()
    timestamp = Timestamp()


class TToken(_BaseTable):
    """
    Table containing mapping of token IDs to user IDs
    """

    user = ForeignKey(TUser)
