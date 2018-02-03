from sqlalchemy import func
from project.models import Answer
from project.settings import SETTINGS

def get_last_answered(session) -> int:
    try:
        return session.query(func.max(Answer.answered_at)).\
            filter_by(survey_id = SETTINGS['SURVEY_ID']).\
            first()[0]
    except TypeError:
        return 0
