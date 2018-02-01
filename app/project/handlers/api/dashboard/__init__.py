"""
API handlers for the Survey task (admin dashboard side)
"""

from datetime import datetime as dt
from hashlib import sha256
from json import dumps

from apistar import http
from apistar.backends.sqlalchemy_backend import Session
from sqlalchemy import func

from project.models import Response
from project.models import Answer

def get_responses(data: http.RequestData, session: Session) -> dict:
    """
    API: Return the most recent 1000 responses, for the admin page.
    """
    items = [{"id": r.id, "started_at": r.started_at,
              "is_completed": r.is_completed,
              "answers": [{"question_id": a.question_id,
                           "in_progress": a.in_progress,
                           "answer": a.answer}
                          for a in session.query(Answer).\
                          filter_by(response_id = r.id).\
                          all()]}
             for r in session.query(Response).\
             order_by(Response.started_at.desc()).\
             limit(1000).all()]

    checksum = sha256(dumps(items).encode('utf-8')).hexdigest()

    try:
        if data['checksum'] == checksum:
            return {}
    except(KeyError, TypeError):
        pass
    
    return {"_items": items, "_items_checksum": checksum}


def get_summary(session: Session) -> dict:
    """
    API: Get a JSON structure of summary data, for the admin page
    """

    try:  # https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query
        num_responses = session.query(func.count(Response.id)).first()[0]
    except Exception:
        num_responses = 0

    try:
        average_age = session.execute('SELECT AVG(CAST(answer AS TINYINT)) FROM answers ' +
                                      'WHERE question_id = %d' % 3).first()[0]
    except Exception:
        average_age = None
        
    gender_ratio = None
    top_3_colors = None
    last_updated = dt.now().isoformat()

    return {"updated_at": last_updated,
            "average_age": average_age,
            "top_3_colors": top_3_colors,
            "gender_ratio": gender_ratio,
            "num_responses": num_responses}
