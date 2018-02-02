"""
API handlers for the Survey task (survey side).
"""

from datetime import datetime as dt

from apistar import http
from apistar.backends.sqlalchemy_backend import Session

from project.models import Question, Response, Answer
from project.utils.validators import validate_answer
from project.settings import SETTINGS


def answer_question(data: http.RequestData, session: Session) -> dict:
    """
    API: POST an answer into the database, from an end-user
    """
    try:
        who:str = data['who']
        question_id:int = int(data['q'][15:])  # remove the 'answer2question' substring
        answer_val:str = data['a']

    except(KeyError, TypeError):
        return {"status":"ERR"}

    try:
        survey_id:int = SETTINGS['SURVEY_ID']
    except KeyError:
        survey_id:int = 0

    question:Question = session.query(Question).get(question_id)

    responder:Response = session.query(Response).\
                         filter(Response.end_user_id == who,
                                Response.survey_id == survey_id).\
                                first()
    
    try:
        answer:Answer = session.query(Answer).filter_by(response_id = responder.id,
                                                        question_id = question.id).\
                                                        first() \
        or Answer(response_id = responder.id,
                  survey_id   = survey_id,
                  question_id = question.id)
        
    except TypeError:
        return {"status":"ERR"}
    
    answer.answered_at = dt.now().timestamp()
    answer.answer = answer_val
    answer.in_progress = 'Y'
    answer.valid_answer = 'Y' if validate_answer(question, answer) else 'N'

    session.add(answer)

    responder.last_at = int(dt.now().timestamp())
    session.add(responder)

    # you can only answer one question at a time really, so answering
    # a question also sets any of your other answers to not 'in progress'
    session.query(Answer).\
        filter(Answer.response_id == responder.id,
               Answer.question_id != question.id,
               Answer.in_progress == 'Y').update({Answer.in_progress: 'N'})
    
    session.commit()

    return {"status":"OK", "validAnswer": bool(answer.valid_answer == 'Y')}


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
