"""
# Backend / Models / Auth config

Configuration of authentication options
"""
from typing import cast
from .tables import TAuthConfig
from backend.util.db_queries import id_exists, get_by_id
from backend.util.auth_check import do_auth_check
from backend.util import http_errors
from backend.types.admin import RequestType


class AuthConfig:
    """
    Represents the auth configuration of the server
    """
    def __init__(self):
        """
        Create an AuthConfig object shadowing the auth configuration for the
        server. This requires the table to be created.
        """
        if not self.exists():
            raise http_errors.BadRequest("AuthConfig hasn't been initialised")
        # Doing the lookup straight away since we'll need to use this info
        # repetitively so frequent lookups are probably slower
        self.__row = get_by_id(TAuthConfig, 1)

    @staticmethod
    def exists() -> bool:
        """
        Returns whether the authentication system has been defined

        ### Returns:
        * `bool`: value
        """
        return id_exists(TAuthConfig, 1)

    @classmethod
    def create(
        cls,
        address: str,
        request_type: RequestType,
        username_param: str,
        password_param: str,
        success_regex: str,
    ) -> 'AuthConfig':
        """
        Create and initialise the auth configuration

        This requires the row in the database to not be initialised

        ### Args:
        * `address` (`str`): address to request for authentication

        * `request_type` (`'get' or 'post`): type of request

        * `username_param` (`str`): parameter to use for username property

        * `password_param` (`str`): parameter to use for password property

        * `success_regex` (`str`): a regular expression to use to check
          authentication. If it matches the request response then
          authentication will be allowed.

        ### Raises:
        * `ValueError`: AuthConfig already initialised

        ### Returns:
        * `AuthConfig`: configuration
        """
        # Make sure it doesn't already exist
        assert not cls.exists()
        TAuthConfig(
            {
                TAuthConfig.address: address,
                TAuthConfig.request_type: request_type,
                TAuthConfig.username_param: username_param,
                TAuthConfig.password_param: password_param,
                TAuthConfig.success_regex: success_regex,
            }
        ).save().run_sync()[0]
        return AuthConfig()

    def _get(self) -> TAuthConfig:
        """
        Return a reference to the underlying database row
        """
        return self.__row

    def authenticate(self, username: str, password: str):
        """
        Attempt to authenticate the user, raising a 401 error if it failed

        ### Args:
        * `username` (`str`): username

        * `password` (`str`): password

        ### Raises:
        * `Forbidden`: if authentication failed
        """
        if not do_auth_check(
            self.address,
            self.request_type,
            self.username_param,
            self.password_param,
            self.success_regex,
            username,
            password,
        ):
            raise http_errors.Forbidden("Incorrect username or password")

    @property
    def address(self) -> str:
        """
        The address to request to when authenticating
        """
        return self._get().address

    # TODO: When we introduce routes to modify the existing auth config,
    # uncomment these
    # @address.setter
    # def address(self, new_address: str):
    #     row = self._get()
    #     row.address = new_address
    #     row.save([TAuthConfig.address]).run_sync()

    @property
    def request_type(self) -> RequestType:
        """
        The request type to make when authenticating
        """
        return cast(RequestType, self._get().request_type)

    # @request_type.setter
    # def request_type(self, new_request_type: RequestType):
    #     row = self._get()
    #     row.request_type = new_request_type
    #     row.save([TAuthConfig.request_type]).run_sync()

    @property
    def username_param(self) -> str:
        """
        The username parameter name to use when authenticating
        """
        return self._get().username_param

    # @username_param.setter
    # def username_param(self, new_username_param: RequestType):
    #     row = self._get()
    #     row.username_param = new_username_param
    #     row.save([TAuthConfig.username_param]).run_sync()

    @property
    def password_param(self) -> str:
        """
        The password parameter name to use when authenticating
        """
        return self._get().password_param

    # @password_param.setter
    # def password_param(self, new_password_param: str):
    #     row = self._get()
    #     row.password_param = new_password_param
    #     row.save([TAuthConfig.password_param]).run_sync()

    @property
    def success_regex(self) -> str:
        """
        The regular expression used to check whether authentication is valid
        """
        return self._get().success_regex

    # @success_regex.setter
    # def success_regex(self, new_success_regex: str):
    #     row = self._get()
    #     row.success_regex = new_success_regex
    #     row.save([TAuthConfig.success_regex]).run_sync()
