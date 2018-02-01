"""
Identity/Authorisation routines.
"""

from datetime import datetime as dt
from hashlib import sha256
from random import SystemRandom

from werkzeug.http import parse_cookie
from apistar.backends.sqlalchemy_backend import Session

from project.models import Response
from project.settings import ENV


def get_identifier(session: Session) -> dict:
    """Based on the incoming request, return a structure containing
    identifying information for this user, and the current
    question/screen we think they're on.
    """
    identifier = None
    screen_no  = None
    
    cookies = parse_cookie(ENV)

    try:
        identifier = cookies.get('eui')
    except KeyError:
        pass

    if not identifier:
        identifier = Response()
        longstring = "{rand}-{time}".\
                     format(rand=''.join([SystemRandom().choice(["abcdefghijklmnopqrstuvwxyz"])
                                          for n in range(10)]),
                            time=dt.now().isoformat())

        identifier.end_user_id = sha256(longstring.encode('utf-8')).hexdigest()
        identifier.started_at = int(dt.now().timestamp())
        identifier.is_completed = ''
        
        session.add(identifier)
        session.commit()

        question_no = 1
    else:
        identifier = session.query(Response).\
                     filter_by(end_user_id = identifier).\
                     first()

        # determine question number
        last_answer = session.query(Answer).\
                      filter_by(response_id = identifier.id).\
                      order_by(Answer.answered_at.desc()).\
                      limit(1).first()

        if last_answer:
            question_no = session.query(Question).get(last_answer.question_id)['order_in_list']
        else:
            question_no = 1
    
    return {"eui": identifier.end_user_id,
            "que": question_no}
