from datetime import datetime
from project.models import Answer

def get_last_answered(session) -> int:
    try:
        return session.query(Answer).filter_by(survey_id = 0).\
            order_by(Answer.answered_at.desc()).limit(1).\
            first().answered_at
    except TypeError:
        return datetime.now().timestamp()
