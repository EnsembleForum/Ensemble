"""
# Backend / Models / Permission Set

Definition for the `PermissionSet` class which defines a set of permissions
that a user has. It also supports derived permissions, meaning that users can
inherit permissions from a general permission set (eg tutors can have
permissions that inherit from the tutor permission set).
"""
from typing import Optional
from .permission import Permission


class PermissionSet:
    """
    Contains a collection of permissions that a user has access to.
    """
    def __init__(
        self,
        name: str,
        parent: Optional['PermissionSet'] = None
    ) -> None:
        """
        Create a permission set.

        ### Args:
        * `parent` (`Optional[PermissionSet]`, optional): permission set to
          derive from. Defaults to `None` to derive from no permissions.
        """
        self.__name = name
        self.__parent = parent
        self.__added: set[Permission] = set()
        self.__subtracted: set[Permission] = set()

    @property
    def name(self) -> str:
        """
        The name of the permission.

        This is used to identify the permission to the user in the UI.

        Read only.
        """
        return self.__name

    @property
    def parent(self) -> Optional['PermissionSet']:
        """
        The parent permission set.

        Represents the permission set that this derives from. This is mainly
        used to assign users special permissions.

        Read/write.
        """
        return self.__parent

    @parent.setter
    def parent(self, new_parent: Optional['PermissionSet']):
        self.__parent = new_parent

    def can(self, action: Permission) -> bool:
        """
        Returns whether this PermissionSet has the ability to perform the
        given action.

        ### Order of checking

        * Return `True` if this permission was added for this set

        * Return `False if this permission was subtracted for this set

        * If there is no parent set, return `False`

        * Otherwise, return the value of `parent.can`

        ### Args:
        * `action` (`Permission`): action to check

        ### Returns:
        * `bool`: whether the action is allowed
        """

    def allow(self, actions: set[Permission]):
        """
        Add the given set of permissions to the allowed set of permissions,
        and remove any elements from the disallowed set of permissions if
        present.

        ### Args:
        * `actions` (`set[Permission]`): action to allow
        """

    def disallow(self, actions: set[Permission]):
        """
        Add the given set of permissions to the disallowed set of permissions,
        and remove any elements from the allowed set of permissions if present.

        ### Args:
        * `actions`: (`set[Permission]`): actions to disallow
        """

    def unassign(self, actions: set[Permission]):
        """
        Unassign the given set of permissions, meaning that they will be
        derived from the parent permissions.

        ### Args:
        * `actions` (`set[Permission]`): actions to remove rules on
        """
