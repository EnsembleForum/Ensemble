"""
# Backend / Models / User
"""
from .tables import TUser
from .permissions import PermissionGroup, PermissionUser
from backend.util.db_queries import id_exists, get_by_id
from backend.types.identifiers import UserId
from typing import cast


class User:
    """
    Represents a user of Ensemble
    """
    # TODO: Flesh this out properly
    def __init__(self, id: UserId):
        """
        Create a user object shadowing an existing in the database

        ### Args:
        * `id` (`int`): user id

        ### Raises:
        * `KeyError`: user does not exist
        """
        if not id_exists(TUser, id):
            raise KeyError(f"Invalid TUser.id {id}")
        self.__id = id

    @classmethod
    def create(
        cls,
        username: str,
        name_first: str,
        name_last: str,
        email: str,
        permissions_base: PermissionGroup
    ) -> 'User':
        """
        Create a new user

        ### Args:
        * `name_first` (`str`): first name

        * `name_last` (`str`): last name

        * `permissions_base` (`PermissionPreset`): permissions to derive this
          user's permissions from.

        ### Returns:
        * `PermissionPreset`: the preset object
        """
        val = TUser(
            {
                TUser.username: username,
                TUser.name_first: name_first,
                TUser.name_last: name_last,
                TUser.email: email,
                TUser.permissions: PermissionUser.create(permissions_base).id,
            }
        ).save().run_sync()[0]
        id = cast(UserId, val["id"])
        return User(id)

    @classmethod
    def all(cls) -> list['User']:
        """
        Returns a list of all users

        ### Returns:
        * `list[User]`: list of users
        """
        return list(map(lambda u: User(u.id), cast(list, TUser.objects())))

    def _get(self) -> TUser:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TUser, self.__id)

    @property
    def id(self) -> int:
        """
        Identifier of the user
        """
        return self.__id

    @property
    def username(self) -> str:
        """
        The username of the user
        """
        return self._get().username

    @username.setter
    def username(self, new_username: str):
        row = self._get()
        row.username = new_username
        row.save().run_sync()

    @property
    def name_first(self) -> str:
        """
        The first name of the user
        """
        return self._get().name_first

    @name_first.setter
    def name_first(self, new_name: str):
        row = self._get()
        row.name_first = new_name
        row.save().run_sync()

    @property
    def name_last(self) -> str:
        """
        The last name of the user
        """
        return self._get().name_last

    @name_last.setter
    def name_last(self, new_name: str):
        row = self._get()
        row.name_last = new_name
        row.save().run_sync()

    @property
    def email(self) -> str:
        """
        The email address of the user
        """
        return self._get().email

    @email.setter
    def email(self, new_email: str):
        row = self._get()
        row.email = new_email
        row.save().run_sync()

    @property
    def permissions(self) -> PermissionUser:
        return PermissionUser(self._get().permissions)
