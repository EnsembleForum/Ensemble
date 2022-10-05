from flask import Blueprint
from backend.types.user import IUserIdList, IUserBasicInfoList, IUserProfile


users = Blueprint('users', 'users')


@users.post('/register')
def register() -> IUserIdList:
    """
    Register a collection of users

    ## Body:
    * `users` (`list[IUserRegisterInfo]`): list of user info to add
    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.

    ## Returns:
    * `IUserIdList`: list of new user IDs
    """


@users.get('/all')
def all() -> IUserBasicInfoList:
    """
    Returns a list of basic info about all forum users

    ### Returns:
    * `IUserBasicInfoList`: list of user info
    """


@users.get('/profile')
def profile() -> IUserProfile:
    """
    Returns detailed info about a user's profile

    ### Returns:
    * `IUserProfile`: list of user info
    """
