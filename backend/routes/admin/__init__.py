"""
# Backend / Routes / Admin

Contains route definitions for functions used with administration
"""
import json
from flask import Blueprint, request
from .permissions import permissions
from .users import users
from .analytics import analytics
from .exam_mode import exam_mode
from backend.models.auth_config import AuthConfig
from backend.types.auth import IAuthInfo
from backend.types.admin import IIsFirstRun
from backend.util import setup


admin = Blueprint('admin', 'admin')

admin.register_blueprint(permissions, url_prefix='/permissions')
admin.register_blueprint(users, url_prefix='/users')
admin.register_blueprint(analytics, url_prefix='/analytics')
admin.register_blueprint(exam_mode, url_prefix='/exam_mode')


@admin.get('/is_first_run')
def is_first_run() -> IIsFirstRun:
    return {"value": not AuthConfig.exists()}


@admin.post('/init')
def init() -> IAuthInfo:
    data = json.loads(request.data.decode('utf-8'))
    address: str = data["address"]
    request_type = str(data["request_type"]).lower()
    username_param: str = data["username_param"]
    password_param: str = data["password_param"]
    success_regex: str = data["success_regex"]
    username: str = data["username"]
    password: str = data["password"]
    email: str = data["email"]
    name_first: str = data["name_first"]
    name_last: str = data["name_last"]
    return setup.init(
        address,
        request_type,
        username_param,
        password_param,
        success_regex,
        username,
        password,
        email,
        name_first,
        name_last,
    )


__all__ = [
    'admin',
]
