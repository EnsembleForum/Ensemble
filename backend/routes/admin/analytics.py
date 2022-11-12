from flask import Blueprint
from backend.types.analytics import IAllStats
from backend.util.tokens import uses_token
from backend.models.user import User
from backend.models.analytics import Analytics
from backend.models.permissions import Permission


analytics = Blueprint('analytics', 'analytics')


@analytics.get('')
@uses_token
def register(user: User, *_) -> IAllStats:
    user.permissions.assert_can(Permission.ViewAnalytics)
    return Analytics.all_stats()
