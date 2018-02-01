"""
"""

from datetime import datetime as dt
from hashlib import sha256
from json import dumps

from apistar import http
from apistar.backends.sqlalchemy_backend import Session
from sqlalchemy import func

from project.models import Response, Answer
from project.settings import SETTINGS

def get_summary(session: Session) -> dict:
    """
    API: Get a JSON structure of summary data, for the admin page
    """

    try:  # https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query
        num_responses = session.query(func.count(func.distinct(Answer.response_id))).first()[0]
    except Exception:
        num_responses = 0

    try:
        average_age = float(session.execute('SELECT AVG(CAST(answer AS UNSIGNED)) FROM answers ' +
                                            'WHERE question_id = %d' % 3).first()[0])
    except Exception:
        average_age = None
        
    gender_ratio = None
    top_3_colors = None

    try:
        last_updated:int = session.query(Answer).filter_by(survey_id = 0).\
                           order_by(Answer.answered_at.desc()).limit(1).\
                           first().answered_at
    except TypeError:
        last_updated:int = dt.now().timestamp()

    return {"updated_at": last_updated,
            "average_age": average_age,
            "colors": top_3_colors,
            "gender_ratio": gender_ratio,
            "num_responses": num_responses}


def get_responses(data: http.RequestData, session: Session) -> dict:
    """
    API: Return the most recent non-empty responses, for the admin page.
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
    
    if 'SHOW_EMPTY_SURVEYS' in SETTINGS and \
       SETTINGS['SHOW_EMPTY_SURVEYS']:
        pass
    else:
        items = list(filter(lambda surv: len(surv['answers']) > 0,
                            items))

    checksum = sha256(dumps(items).encode('utf-8')).hexdigest()

    try:
        if data['checksum'] == checksum:
            return {}
    except(KeyError, TypeError):
        pass

    # add a count of all of them
    try:
        surveys_count = int(session.\
                            execute('SELECT COUNT(DISTINCT(response_id)) ' + \
                                    'FROM answers WHERE survey_id = %d ' %
                                    SETTINGS['SURVEY_ID']).first()[0])
    except Exception:
        surveys_count = 0
        
    
    return {"_items": items, "_items_checksum": checksum, "count": surveys_count}
