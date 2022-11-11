from flask import Blueprint
from backend.types.analytics import IAllStats
from backend.util.tokens import uses_token
from backend.models.user import User
from backend.models.analytics import Analytics


analytics = Blueprint('analytics', 'analytics')


@analytics.get('')
@uses_token
def register(user: User, *_) -> IAllStats:
    return Analytics.all_stats(user)
