"""
Identity/Authorisation routines.
"""

from datetime import datetime as dt
from hashlib import sha256
from random import SystemRandom

from werkzeug.http import parse_cookie
from apistar.backends.sqlalchemy_backend import Session

from project.models import Question, Response, Answer
from project.settings import ENV


def extract_identifier():
    """
    Return the 'eui' cookie from the environment, or None
    """
    cookies = parse_cookie(ENV)

    try:
        id:str = cookies.get('eui')
    except KeyError:
        id:NoneType = None

    return id


def make_new_response(session: Session) -> Response:
    """
    Generate a new SHA identifier
    """
    identifier = Response()
    longstring = "{rand}-{time}".\
                 format(rand=''.join([SystemRandom().choice(["abcdefghijklmnopqrstuvwxyz"])
                                      for n in range(100)]),
                        time=dt.now().isoformat())
    
    identifier.end_user_id = sha256(longstring.encode('utf-8')).hexdigest()
    identifier.started_at = int(dt.now().timestamp())
    identifier.is_completed = ''
        
    session.add(identifier)
    session.commit()

    return identifier


def get_identifier(session: Session) -> dict:
    """Based on the incoming request, return a dict containing
    identifying information for this user, and the current
    question/screen we think they're on.
    """
    responder:Response = session.query(Response).\
                         filter_by(end_user_id = extract_identifier()).\
                         first() or make_new_response(session)   # simple factory
        
    try:
        current_question_no:int = get_highest_completed_question(session, responder)['order_in_list'] + 1
    except TypeError:
        current_question_no:int = 1
        
    return {"eui": responder.end_user_id,
            "que": current_question_no}


def get_highest_completed_question(session: Session, identifier: Response) -> Question:
    """
    Return the most recent Question that this person answered.
    """
    last_answer:Answer = session.query(Answer).\
                         filter_by(response_id = identifier.id,
                                   in_progress = 'N').\
                         order_by(Answer.answered_at.desc()).\
                         limit(1).first()

    try:
        return session.query(Question).get(last_answer.question_id)
    except AttributeError:
        return None
