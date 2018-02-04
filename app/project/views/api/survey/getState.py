from apistar import http
from apistar.backends.sqlalchemy_backend import Session
from project.models import Response, Answer
from project.views.api import get_questions

def get_state(data: http.RequestData, session: Session) -> dict:
    """For a returning user with id string in param 'i', return a JSON
    structure indicating where they are in the process.
    """
    try:
        responder:Response = session.query(Response).\
                             filter_by(end_user_id = data['i']).\
                             first()
    except(TypeError, KeyError):
        return {}

    if not responder:
        return {}
    
    if responder.is_completed == 'Y':
        return {"complete":True}
    else:
        answers:list = session.query(Answer).\
                       filter_by(response_id = responder.id).\
                       limit(1000).all()
        
        return {"answers": [{"question_id": a.question_id,
                             "answer": a.answer,
                             "in_progress": a.in_progress,
                             "valid_answer": a.valid_answer}
                            for a in answers],
                "questions": get_questions(session)}
