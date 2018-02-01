"""
API handlers for the Survey task (survey side).
"""

from datetime import datetime as dt

from apistar import http
from apistar.backends.sqlalchemy_backend import Session

from project.models import Question
from project.models import Response
from project.models import Answer

from project.utils import validate_answer


def answer_question(data: http.RequestData, session: Session) -> dict:
    """
    API: POST an answer into the database, from an end-user
    """
    try:
        who = data['who']
        question_id = int(data['q'][15:])  # remove the 'answer2question' substring
        answer_val = data['a']
    except(KeyError, TypeError):
        return {"status":"ERR"}

    # get the responder (the 'who')
    responder = session.query(Response).\
                filter(Response.end_user_id == who,
                       Response.survey_id >= 0).\
                first()
    
    # get the question
    question = session.query(Question).get(question_id)

    if not (responder and question):
        return {"status":"ERR"}
    
    #
    # new or existing answer
    answer = session.query(Answer).filter_by(response_id = responder.id,
                                             question_id = question.id).first()

    if not answer:
        answer = Answer(response_id = responder.id,
                        question_id = question.id)

    answer.answered_at = dt.now().timestamp()
    answer.answer = answer_val
    answer.in_progress = 'Y'
    session.add(answer)

    # you can only answer one question at a time really, so answering
    # a question also sets any of your other answers to not 'in progress'
    session.query(Answer).\
        filter(Answer.response_id == responder.id,
               Answer.question_id != question.id,
               Answer.in_progress == 'Y').update({Answer.in_progress: 'N'})
    
    session.commit()

    validAnswer = validate_answer(question, answer)
    
    return {"status":"OK", "validAnswer": validAnswer}
