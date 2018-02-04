from sqlalchemy import func
from project.models import Answer


class countSurveysBehaviour():

    def __init__(self) -> None:
        pass
    
    def getResult(self, session) -> int:
        """Counts distinct responses in answers, using sqlalchemy's func.
        (This avoids counting completely-blank surveys, which we don't
        display anyway.)
        """
        try:
            return session.query(func.count(func.distinct(Answer.response_id))).first()[0]
        except Exception:
            return 0
