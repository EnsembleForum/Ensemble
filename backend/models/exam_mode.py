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

    def _get(self) -> TExamMode:
        """
        Return a reference to the underlying database row
        """
        return get_by_id(TExamMode, 1)

    def turn_on(self):
        """
        Turn on exam mode
        """
        row = self._get()
        row.exam_mode = True
        row.save().run_sync()

    def turn_off(self):
        """
        Turn off exam mode
        """
        row = self._get()
        row.exam_mode = False
        row.save().run_sync()

    @property
    def is_on(self) -> bool:
        return self._get().exam_mode

    @classmethod
    def exam_mode_toggle(cls, self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
