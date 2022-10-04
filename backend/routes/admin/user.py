from flask import Blueprint
from backend.types.user import IUserIdList


user = Blueprint('users', 'users')


@user.post('/register')
def register() -> IUserIdList:
    """
    Register a collection of users

    ## Body:
    * `users` (`list[IUserBasicDetails]`): list of user info to add
    * `group_id` (`PermissionGroupId`): permission group ID to assign all users
      to.
    """
