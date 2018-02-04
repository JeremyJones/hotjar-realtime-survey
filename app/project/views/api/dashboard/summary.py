from datetime import datetime as dt
from sqlalchemy import func
from apistar import http
from apistar.backends.sqlalchemy_backend import Session

from project.models import Answer
from project.models.dashboard.summary import Summariser
        
def get_summary(session: Session) -> dict:
    """
    API: Get a JSON structure of summary data, for the admin page
    """
    s = Summariser()  # could substitute different behaviours e.g. if requested via the POST data

    return {
        "num_responses": s.countSurveys(session),
        "average_age": s.averageAge(session),
        "gender_ratio": s.genderRatio(session),
        "top_3_colors": s.topColours(session),
        "updated_at": s.lastAnswered(session)
    }
