"""
# Backend / Models / Permissions / Permission Set

Definition for the `PermissionSet` class which defines a set of permissions
that a user has. It also supports derived permissions, meaning that users can
inherit permissions from a general permission set (eg tutors can have
permissions that inherit from the tutor permission set).
"""
from typing import Optional
from .permission import Permission
from ..tables import TPermissionGroup, TPermissionUser
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.exceptions import PermissionError
from backend.types.identifiers import UserPermissionId, PermissionGroupId
from backend.types.permissions import (
    IPermissionValueGroup,
    IPermissionValueUser,
)
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

    def assert_can(self, action: Permission) -> None:
        """
        Ensures that a user can perform an action.

        If they cannot, a PermissionError is raised

        ### Args:
        * `action` (`Permission`): permission to check
        """
        if not self.can(action):
            raise PermissionError(
                f"You don't have the {action.name} permission"
            )


class PermissionGroup(PermissionSet):
    """
    Represents a permission group, from which user permissions are derived.
    """

    def __init__(self, id: PermissionGroupId):
        """
        Load a permission group from the database

        ### Args:
        * `id` (`int`): ID of the preset
        """
        assert_id_exists(TPermissionGroup, id)
        self.__id = id

    @classmethod
    def create(
        cls,
        name: str,
        options: dict[Permission, bool]
    ) -> 'PermissionGroup':
        """
        Create a new permission group and store it into the database

        ### Args:
        * `name` (`str`): name of preset

        * `options` (`dict[Permission, Optional[bool]]`): allowed and
          disallowed permissions.

        ### Returns:
        * `PermissionGroup`: the permission group object
        """
        val = TPermissionGroup(
            {
                TPermissionGroup.name: name,
                TPermissionGroup.allowed: [],
                TPermissionGroup.disallowed: [],
            }
        ).save().run_sync()[0]
        id = cast(PermissionGroupId, val["id"])
        ret = PermissionGroup(id)
        ret.update_allowed(options)
        return ret

    @classmethod
    def all(cls) -> list['PermissionGroup']:
        """
        Returns a list of all available permission groups
        """
        ids = TPermissionGroup.select(TPermissionGroup.id).run_sync()
        return [cls(i['id']) for i in ids]

    def delete(self) -> None:
        """
        Delete this permission group
        """
        TPermissionGroup.delete()\
            .where(TPermissionGroup.id == self.id)\
            .run_sync()

    def _get(self) -> TPermissionGroup:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TPermissionGroup, self.__id)

    @property
    def id(self) -> PermissionGroupId:
        """
        Identifier of this permission group
        """
        return self.__id

    @property
    def name(self) -> str:
        """
        The name of the permission group (eg 'Tutor')
        """
        return self._get().name

    @name.setter
    def name(self, new_name: str):
        row = self._get()
        row.name = new_name
        row.save().run_sync()

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

    def update_allowed(self, actions: dict[Permission, bool]):
        """
        Add the given set of permissions to the allowed set of permissions,
        and remove any elements from the disallowed set of permissions if
        present.

        ### Args:
        * `actions` (`dict[Permission, Optional[bool]]`): dictionary of
          permissions to allow or disallow. Each Permission should be set to
          `True` to allow, `False` to disallow.
        """
        row = get_by_id(TPermissionGroup, self.__id)

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

        row.save([TPermissionGroup.allowed, TPermissionGroup.disallowed])\
            .run_sync()


class PermissionUser(PermissionSet):
    """
    Represents a user permission, which derives from a group.
    """

    def __init__(self, id: UserPermissionId) -> None:
        """
        Load a user permission set from the database

        ### Args:
        * `id` (`int`): ID of the preset
        """
        assert_id_exists(TPermissionUser, id)
        self.__id = id

    @classmethod
    def create(cls, parent: PermissionGroup) -> 'PermissionUser':
        """
        Create a user permission set and store it into the database.

        ### Args:
        * `parent` (`PermissionGroup`): parent permission set

        ### Returns:
        * `Self`: PermissionUser
        """
        val = TPermissionUser(
            {
                TPermissionUser.parent: parent.id,
                TPermissionGroup.allowed: [],
                TPermissionGroup.disallowed: [],
            }
        ).save().run_sync()[0]
        id = cast(UserPermissionId, val["id"])
        ret = PermissionUser(id)
        return ret

    def delete(self) -> None:
        """
        Delete this user permission set
        """
        TPermissionUser.delete()\
            .where(TPermissionUser.id == self.id)\
            .run_sync()

    def _get(self) -> TPermissionUser:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TPermissionUser, self.__id)

    @property
    def id(self) -> UserPermissionId:
        """
        Identifier of this user permission set
        """
        return self.__id

    @property
    def parent(self) -> PermissionGroup:
        """
        The parent permissions for this user permission set

        ### Returns:
        * `PermissionPreset`: the parent preset
        """
        return PermissionGroup(self._get().parent)

    @parent.setter
    def parent(self, new_parent: PermissionGroup):
        row = self._get()
        row.parent = new_parent.id
        row.save().run_sync()

    def can(self, action: Permission) -> bool:
        row = self._get()
        if action.value in row.allowed:
            return True
        elif action.value in row.disallowed:
            return False
        else:
            return self.parent.can(action)

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
        row = get_by_id(TPermissionGroup, self.__id)

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

        row.save([TPermissionGroup.allowed, TPermissionGroup.disallowed])\
            .run_sync()


def map_permissions_group(
    permissions: list[IPermissionValueGroup]
) -> dict[Permission, bool]:
    """
    Maps group permission values from a list into a dictionary

    ### Args:
    * `permissions` (`list[IPermissionValueGroup]`): list of permission values

    ### Returns:
    * `dict[Permission, bool]`: dictionary of mappings
    """
    mapped_perms: dict[Permission, bool] = {}
    for p in permissions:
        mapped_perms[Permission(p['permission_id'])] = p['value']
    return mapped_perms


def map_permissions_user(
    permissions: list[IPermissionValueUser]
) -> dict[Permission, bool | None]:
    """
    Maps user permission values from a list into a dictionary

    ### Args:
    * `permissions` (`list[IPermissionValueUser]`): list of permission values

    ### Returns:
    * `dict[Permission, bool]`: dictionary of mappings
    """
    mapped_perms: dict[Permission, bool | None] = {}
    for p in permissions:
        mapped_perms[Permission(p['permission_id'])] = p['value']
    return mapped_perms
