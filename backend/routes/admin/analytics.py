from flask import Blueprint
from backend.types.analytics import IAllStats
from backend.util.tokens import uses_token
from backend.models import User, Analytics, Permission


analytics = Blueprint('analytics', 'analytics')


@analytics.get('')
@uses_token
def get_analytics(user: User, *_) -> IAllStats:
    user.permissions.assert_can(Permission.ViewAnalytics)
    return Analytics.all_stats()
