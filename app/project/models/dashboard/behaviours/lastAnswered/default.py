from sqlalchemy import func
from project.models import Answer
from project.settings import SETTINGS


class lastAnsweredBehaviour():

    default_survey_id:int = SETTINGS['SURVEY_ID']

    def __init__(self, survey_id=None) -> None:
        self.survey_id:int = survey_id or self.default_survey_id

    def get_survey_id(self) -> int:
        return self.survey_id

    def getResult(self, session) -> int:
        try:
            return session.query(func.max(Answer.answered_at)).\
                filter_by(survey_id = self.get_survey_id()).\
                first()[0]
        except TypeError:
            return 0
