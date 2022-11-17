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
    pronouns = Text(null=True)
    permissions = ForeignKey(TPermissionUser)


class TQueue(_BaseTable):
    immutable = Boolean()
    view_only = Boolean()
    name = Text()


class TQueueFollow(_BaseTable):
    """
    Relationship for who follows what queues
    """
    user = ForeignKey(TUser)
    queue = ForeignKey(TQueue)


class TPost(_BaseTable):
    """
    Table containing all posts
    """

    author = ForeignKey(TUser)
    heading = Text()
    text = Text()
    timestamp = Timestamp()
    queue = ForeignKey(TQueue)
    private = Boolean()
    anonymous = Boolean()
    answered = Integer(null=True)
    # FIXME
    # answered = ForeignKey("TComment", null=True)
    # For some reason this causes an error:
    # ValueError: Can't find a Table subclass called
    # TComment in backend.models.tables


class TTag(_BaseTable):
    name = Text()


class TPostTags(_BaseTable):
    tag = ForeignKey(TTag)
    post = ForeignKey(TPost)


class TComment(_BaseTable):
    """
    Table containing all comments
    """

    author = ForeignKey(TUser)
    parent = ForeignKey(TPost)
    deleted = Boolean()
    text = Text()
    timestamp = Timestamp()


class TReply(_BaseTable):
    """
    Table containing all replies
    """

    author = ForeignKey(TUser)
    parent = ForeignKey(TComment)
    deleted = Boolean()
    text = Text()
    timestamp = Timestamp()


class TPostReacts(_BaseTable):
    """
    Table containing reactions to a post
    """

    user = ForeignKey(TUser)
    post = ForeignKey(TPost)


class TCommentReacts(_BaseTable):
    """
    Table containing reactions to a comment
    """

    user = ForeignKey(TUser)
    comment = ForeignKey(TComment)


class TReplyReacts(_BaseTable):
    """
    Table containing reactions to a reply
    """

    user = ForeignKey(TUser)
    reply = ForeignKey(TReply)


class TToken(_BaseTable):
    """
    Table containing mapping of token IDs to user IDs
    """

    user = ForeignKey(TUser)


class TNotification(_BaseTable):
    """
    Table containing notifications
    """

    notif_type = Integer()
    """Type of notification (as per notifications.NotificationType)"""

    user_to = ForeignKey(TUser)
    """User the notification is directed to"""

    seen = Boolean()
    """Whether the notification has been seen"""

    timestamp = Timestamp()
    """When the notification was sent"""

    user_from = ForeignKey(TUser, null=True)
    """User who gave the notification, if any"""

    post = ForeignKey(TPost, null=True)
    """Post the notification is related to"""

    comment = ForeignKey(TComment, null=True)
    """Comment the notification is related to"""

    reply = ForeignKey(TReply, null=True)
    """Reply the notification is related to"""

    queue = ForeignKey(TQueue, null=True)
    """Queue the notification is related to"""


class TExamMode(_BaseTable):
    """
    Table storing whether exam mode is on or off
    """

    exam_mode = Boolean()
