"""
# Backend / Types / Identifiers

Identifier types used for additional type safety.

These are used to prevent interchangeability between different types of
identifiers.
"""


class Identifier(int):
    """
    Base class for identifiers used within the application.
    """


class UserId(Identifier):
    """
    Identifier for a user
    """


class TokenId(Identifier):
    """
    Identifier for a token
    """


class PermissionId(Identifier):
    """
    Identifier for a permission
    """


class UserPermissionId(Identifier):
    """
    Identifier for a user's permission table entry
    """


class PermissionGroupId(Identifier):
    """
    Identifier for a permission group
    """


class PostId(Identifier):
    """
    Identifier for a post
    """


class CommentId(Identifier):
    """
    Identifier for a comment
    """


class ReplyId(Identifier):
    """
    Identifier for a reply
    """


class QueueId(Identifier):
    """
    Identifier for a queue
    """

class FeedbackId(Identifier):
    """
    Identifier for a feedback
    """
