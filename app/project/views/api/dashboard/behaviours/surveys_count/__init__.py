from sqlalchemy import func
from project.models import Answer

def get_surveys_count(session) -> int:
    try:
        return session.query(func.count(func.distinct(Answer.response_id))).first()[0]
    except Exception:
        return 0
