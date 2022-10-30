"""
# Backend / Models / User
"""
from .tables import TUser
from .permissions import PermissionGroup, PermissionUser
from backend.util.exceptions import MatchNotFound
from backend.util.db_queries import assert_id_exists, get_by_id
from backend.util.validators import assert_email_valid, assert_valid_str_field
from backend.types.identifiers import UserId
from backend.types.user import IUserProfile, IUserBasicInfo
from typing import cast


class User:
    """
    Represents a user of Ensemble
    """
    def __init__(self, id: UserId):
        """
        Create a user object shadowing an existing in the database

        ### Args:
        * `id` (`int`): user id

        ### Raises:
        * `BadRequest`: user does not exist
        """
        assert_id_exists(TUser, id)
        self.__id = id

    @classmethod
    def create(
        cls,
        username: str,
        name_first: str,
        name_last: str,
        email: str,
        pronoun: str,
        permissions_base: PermissionGroup
    ) -> 'User':
        """
        Create a new user

        ### Args:
        * `username` (`str`): username

        * `name_first` (`str`): first name

        * `name_last` (`str`): last name

        * `pronoun` (`str`): pronoun

        * `email` (`str`): email address

        * `permissions_base` (`PermissionPreset`): permissions to derive this
          user's permissions from.

        ### Returns:
        * `PermissionPreset`: the preset object
        """
        assert_valid_str_field(username, "Username")
        if email is not None:
            assert_email_valid(email)
        val = TUser(
            {
                TUser.username: username,
                TUser.name_first: name_first,
                TUser.name_last: name_last,
                TUser.email: email,
                TUser.pronoun: pronoun,
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
        return list(map(
            lambda u: User(u.id),
            cast(list, TUser.objects().run_sync())
        ))

    @classmethod
    def from_username(cls, username: str) -> 'User':
        """
        Find a user based on their username

        ### Args:
        * `username` (`str`): username

        ### Returns:
        * `User`: user object
        """
        result = TUser.objects()\
            .where(TUser.username == username)\
            .first()\
            .run_sync()
        if result is None:
            raise MatchNotFound(f"User with username {username} not found")
        return User(result.id)

    @classmethod
    def from_email(cls, email: str) -> 'User':
        """
        Find a user based on their email

        ### Args:
        * `email` (`str`): email

        ### Returns:
        * `User`: user object
        """
        result = TUser.objects()\
            .where(TUser.email == email)\
            .first()\
            .run_sync()
        if result is None:
            raise MatchNotFound(f"User with email {email} not found")
        return User(result.id)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, User):
            return self.id == __o.id
        else:
            return False

    def _get(self) -> TUser:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TUser, self.__id)

    @property
    def id(self) -> UserId:
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

    @property
    def name_first(self) -> str:
        """
        The first name of the user
        """
        return self._get().name_first

    @name_first.setter
    def name_first(self, new_name: str):
        assert_valid_str_field(new_name, "First name")
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
        assert_valid_str_field(new_name, "Last name")
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
        assert_email_valid(new_email)
        row = self._get()
        row.email = new_email
        row.save().run_sync()

    @property
    def pronoun(self) -> str:
        return self._get().pronoun

    @pronoun.setter
    def pronoun(self, new_pronoun: str):
        assert_valid_str_field(new_pronoun, "Pronoun")
        row = self._get()
        row.email = new_pronoun
        row.save().run_sync()

    @property
    def permissions(self) -> PermissionUser:
        return PermissionUser(self._get().permissions)

    def basic_info(self) -> IUserBasicInfo:
        """
        Returns basic info on the user

        ### Returns:
        * `IUserBasicInfo`: basic info
        """
        row = self._get()
        return {
            "name_first": row.name_first,
            "name_last": row.name_last,
            "pronoun": row.pronoun,
            "username": row.username,
            "user_id": UserId(row.id),
        }

    def profile(self) -> IUserProfile:
        """
        Returns full profile info on the user

        ### Returns:
        * `IUserProfile`: full profile info
        """
        row = self._get()
        return {
            "name_first": row.name_first,
            "name_last": row.name_last,
            "username": row.username,
            "pronoun": row.pronoun,
            "user_id": UserId(row.id),
            "email": row.email,
        }
