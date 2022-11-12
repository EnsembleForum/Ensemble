"""
# Backend / Models / Exam Mode
"""
from .tables import TExamMode
from backend.util.db_queries import get_by_id, id_exists


class ExamMode:
    """
    Represents Exam Mode of Ensemble
    """

    @classmethod
    def initialise(cls):
        """
        Initialises the exam mode table and sets exam mode to false
        """
        if not id_exists(TExamMode, 1):
            TExamMode(
                {
                    TExamMode.exam_mode: False,
                }
            ).save().run_sync()

    @classmethod
    def _get(cls) -> TExamMode:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TExamMode, 1)

    @classmethod
    def enable(cls):
        """
        Turn on exam mode
        """
        row = cls._get()
        row.exam_mode = True
        row.save().run_sync()

    @classmethod
    def disable(cls):
        """
        Turn off exam mode
        """
        row = cls._get()
        row.exam_mode = False
        row.save().run_sync()

    @classmethod
    def is_enabled(cls) -> bool:
        return cls._get().exam_mode

    @classmethod
    def exam_mode_toggle(cls):
        if cls.is_enabled():
            cls.disable()
        else:
            cls.enable()
