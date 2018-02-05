from apistar.backends.sqlalchemy_backend import Session

from project.models import Question
from project.settings import SETTINGS


def get_questions(session: Session) -> dict:
    """
    API: Retrieve a list of the questions in JSON format
    """
    queryset = session.query(Question).\
               filter_by(survey_id = SETTINGS['SURVEY_ID']).\
               order_by(Question.order_in_list).\
               all()
    
    return {"_items": [{"question": question.question,
                        "required": question.required,
                        "id": question.id,
                        "answer_type": question.answer_type,
                        "answer_options": question.answer_options}
                       for question in queryset]
    }
