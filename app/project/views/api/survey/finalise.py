from datetime import datetime as dt

from apistar import http
from apistar.backends.sqlalchemy_backend import Session

from project.models import Question, Response, Answer
from project.utils.validators import validate_answer
from project.settings import SETTINGS

def finalise(data: http.RequestData, session: Session) -> dict:
    """
    API: Complete a survey
    """
    try:
        who:str = data['who']
    except TypeError:
        return {}

    responder:Response = session.query(Response).\
                         filter(Response.end_user_id == who,
                                Response.is_completed == '').first()

    try:
        responder.is_completed = 'Y'
    except AttributeError:
        return {}
    else:
        session.add(responder)

        session.query(Answer).\
            filter(Answer.response_id == responder.id,
                   Answer.in_progress == 'Y').update({Answer.in_progress: 'N'})

        return {"status":"OK"}
