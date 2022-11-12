from flask import Blueprint
from backend.types.exam_mode import IExamModeInfo
from backend.util.tokens import uses_token
from backend.models.user import User
from backend.models.exam_mode import ExamMode
from backend.models.permissions import Permission


exam_mode = Blueprint('exam_mode', 'exam_mode')


@exam_mode.get('/is_enabled')
@uses_token
def is_enabled(user: User, *_) -> IExamModeInfo:
    user.permissions.assert_can(Permission.PostView)
    return {
        'is_enabled': ExamMode.is_enabled()
    }


@exam_mode.put('/toggle')
@uses_token
def exam_mode_toggle(user: User, *_) -> IExamModeInfo:
    user.permissions.assert_can(Permission.SetExamMode)
    ExamMode.exam_mode_toggle()
    return {
        'is_enabled': ExamMode.is_enabled()
    }
