"""
# Backend / Models / Permissions / Permission Set

Definition for the `PermissionSet` class which defines a set of permissions
that a user has. It also supports derived permissions, meaning that users can
inherit permissions from a general permission set (eg tutors can have
permissions that inherit from the tutor permission set).
"""
from typing import Optional
from .permission import Permission
from ..tables import TPermissionPreset, TPermissionUser
from backend.util.db_queries import id_exists, get_by_id
from abc import abstractmethod
from typing import cast


class PermissionSet:
    """
    Contains a collection of permissions that a user has access to.

    This is an abstract class. Don't instantiate it. Instead, create an
    instance of:

    * `PermissionPreset` for a preset that users can inherit from
    * `PermissionUser` for a specific user's permissions
    """

    @abstractmethod
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

    @abstractmethod
    def update_allowed(self, actions: dict[Permission, Optional[bool]]):
        """
        Add the given set of permissions to the allowed set of permissions,
        and remove any elements from the disallowed set of permissions if
        present.

        ### Args:
        * `actions` (`dict[Permission, Optional[bool]]`): dictionary of
          permissions to allow or disallow. Each Permission should be set to
          `True` to allow, `False` to disallow, or `None` to leave as default.
        """


class PermissionPreset(PermissionSet):
    """
    Represents a preset permission, from which user permissions are derived.
    """
    def __init__(self, id: int):
        """
        Load a permission preset from the database

        ### Args:
        * `id` (`int`): ID of the preset
        """
        if not id_exists(TPermissionPreset, id):
            raise KeyError(f"Invalid PermissionPreset.id {id}")
        self.__id = id

    @classmethod
    def create(
        self,
        name: str,
        options: dict[Permission, Optional[bool]]
    ) -> 'PermissionPreset':
        """
        Create a new permission preset

        ### Args:
        * `name` (`str`): name of preset

        * `options` (`dict[Permission, Optional[bool]]`): allowed and
          disallowed permissions.

        ### Returns:
        * `PermissionPreset`: the preset object
        """
        val = TPermissionPreset(
            {
                TPermissionPreset.name: name,
                TPermissionPreset.allowed: [],
                TPermissionPreset.disallowed: [],
            }
        ).save().run_sync()
        id = cast(bool, val.id)
        return PermissionPreset(id)

    def _get(self) -> TPermissionPreset:
        """
        Return a reference to the underlying database column
        """
        return get_by_id(TPermissionPreset, self.__id)

    @property
    def id(self) -> int:
        """
        Identifier of this permission preset
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        The name of the permission preset (eg 'Tutor')
        """
        return self._get().name

    @name.setter
    def name(self, new_name: str):
        row = self._get()
        row.name = new_name
        row.save()

    def can(self, action: Permission) -> bool:
        row = self._get()
        if action.value in row.allowed:
            return True
        elif action.value in row.disallowed:
            return False
        # IDEA: Could have a global permission which also applies to users that
        # have not logged in?
        else:
            return False

    def update_allowed(self, actions: dict[Permission, Optional[bool]]):
        row = get_by_id(TPermissionPreset, self.__id)

        allowed: list[int] = []
        disallowed: list[int] = []

        for act, option in actions.items():
            if option is None:
                continue
            elif option:
                allowed.append(act.value)
            else:
                disallowed.append(act.value)

        row.allowed = allowed
        row.disallowed = disallowed

        row.save([TPermissionPreset.allowed, TPermissionPreset.disallowed])


class PermissionUser(PermissionSet):
    """
    Represents a user permission, which derives from a preset.
    """
    def __init__(self, id: int) -> None:
        """
        Load a user permission set from the database

        ### Args:
        * `id` (`int`): ID of the preset
        """
        if not id_exists(TPermissionUser, id):
            raise KeyError(f"Invalid PermissionUser.id {id}")
        self.__id = id

    @property
    def id(self) -> int:
        """
        Identifier of this permission preset
        """
        return self.__id

    @property
    def owner(self) -> str:
        """
        The user that this permission belongs to
        """
        return self._get().name
