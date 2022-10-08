"""
# Backend / Models / Auth config

Configuration of authentication options
"""
from .tables import TAuthConfig
from backend.util.db_queries import id_exists, get_by_id
import re
import requests
from typing import Literal


class AuthConfig:
    """
    Represents the auth configuration of the server
    """
    def __init__(self):
        """
        Create an AuthConfig object shadowing the auth configuration for the
        server. This requires the table to be created.
        """
        if not id_exists(TAuthConfig, 1):
            raise ValueError("AuthConfig hasn't been initialised")
        self.__id = 1

    @classmethod
    def create(
        cls,
        address: str,
        request_type: Literal['get', 'post'],
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
        try:
            AuthConfig()
        except ValueError:
            pass
        else:
            raise ValueError("AuthConfig has already been initialised")
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
        return get_by_id(TAuthConfig, self.__id)

    def authenticate(self, username: str, password: str) -> bool:
        """
        Attempt to authenticate the user and return whether it worked

        ### Args:
        * `username` (`str`): username

        * `password` (`str`): password

        ### Returns:
        * `bool`: whether authentication was a success
        """
        if self.request_type == "get":
            res = requests.get(
                self.address,
                params={
                    self.username_param: username,
                    self.password_param: password,
                }
            )
        else:
            res = requests.post(
                self.address,
                json={
                    self.username_param: username,
                    self.password_param: password,
                }
            )
        return re.match(self.success_regex, res.text) is not None

    @property
    def address(self) -> str:
        """
        The address to request to when authenticating
        """
        return self._get().address

    @address.setter
    def address(self, new_address: str):
        row = self._get()
        row.address = new_address
        row.save().run_sync()

    @property
    def request_type(self) -> str:
        """
        The request type to make when authenticating
        """
        return self._get().request_type

    @request_type.setter
    def request_type(self, new_request_type: Literal['get', 'post']):
        row = self._get()
        row.request_type = new_request_type
        row.save().run_sync()

    @property
    def username_param(self) -> str:
        """
        The username parameter name to use when authenticating
        """
        return self._get().username_param

    @username_param.setter
    def username_param(self, new_username_param: Literal['get', 'post']):
        row = self._get()
        row.username_param = new_username_param
        row.save().run_sync()

    @property
    def password_param(self) -> str:
        """
        The password parameter name to use when authenticating
        """
        return self._get().password_param

    @password_param.setter
    def password_param(self, new_password_param: Literal['get', 'post']):
        row = self._get()
        row.password_param = new_password_param
        row.save().run_sync()

    @property
    def success_regex(self) -> str:
        """
        The regular expression used to check whether authentication is valid
        """
        return self._get().success_regex

    @success_regex.setter
    def success_regex(self, new_success_regex: Literal['get', 'post']):
        row = self._get()
        row.success_regex = new_success_regex
        row.save().run_sync()
