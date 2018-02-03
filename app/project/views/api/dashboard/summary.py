from datetime import datetime as dt
from sqlalchemy import func

from project.models import Answer
from .behaviours.surveys_count import get_surveys_count
from .behaviours.average_age import get_average_age
from .behaviours.gender_ratio import get_gender_ratio
from .behaviours.top_3_colors import get_top_3_colors
from .behaviours.last_answered import get_last_answered


def get_summary(session) -> dict:
    """
    API: Get a JSON structure of summary data, for the admin page
    """
    return {
        "num_responses": get_surveys_count(session),
        "average_age": get_average_age(session),
        "gender_ratio": get_gender_ratio(session),
        "top_3_colors": get_top_3_colors(session)
        "updated_at": get_last_answered(session)
    }
