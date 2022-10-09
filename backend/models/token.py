"""
# Backend / Models / Token
"""
import jwt
from .tables import TToken
from .user import User
from backend.types.identifiers import TokenId
from backend.util.db_queries import id_exists, get_by_id
from backend.util import http_errors
from typing import cast


SECRET = (  # TODO
    "Using a string constant as a secret is a terrible idea, and we need "
    "to come up with a better solution before the final sprint! "
    "Optimally, our solution would be to regenerate a secret that can be "
    "securely stored, so that it's different for every instance of the server."
)


class Token:
    """
    Represents a JWT (JSON web token) used by a user to allow them to
    authenticate
    """
    def __init__(self, id: TokenId) -> None:
        # TODO: Replace with check_id_exists when merged
        if not id_exists(TToken, id):
            raise KeyError(f"Invalid TUser.id {id}")
        self.__id = id

    def _get(self) -> TToken:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TToken, self.__id)

    @classmethod
    def create(self, user: 'User') -> 'Token':
        """
        Create a new token used by the given user

        ### Args:
        * `user` (`User`): user to associate token with

        ### Returns:
        * `Token`: token
        """
        val = TToken(
            {
                TToken.user: user.id
            }
        ).save().run_sync()[0]
        id = cast(TokenId, val["id"])
        return Token(id)

    @classmethod
    def fromJWT(self, token: str) -> 'Token':  # TODO: replace type to JWT
        """
        Get a token given a JWT string

        This expects the token to exist in the database.

        ### Args:
        * `jwt` (`str`): JWT string

        ### Returns:
        * `Token`: token object
        """
        decoded = jwt.decode(token, key=SECRET)
        user_id = decoded["user_id"]
        token_id = decoded["token_id"]
        t = Token(token_id)
        if t.user.id != user_id:
            raise http_errors.Forbidden(
                "The user associated with this token doesn't "
                "match the information stored on the server."
            )
        return t

    @property
    def user(self) -> User:
        """
        Returns a reference to the user that owns this token

        ### Returns:
        * `User`: user
        """
        return User(self._get().user)
