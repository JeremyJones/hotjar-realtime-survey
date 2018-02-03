from re import match

from project.models import Question, Answer

from .valid_string import valid_string
from .valid_email import valid_email
from .valid_select import valid_select

def validate_answer(question: Question, answer: Answer) -> bool:
    """Given a Question and Answer object, return True/False if the
    answer given is a valid answer according to that question's
    validation rules (e.g. email etc.).
    """
    if question.required == 'n':
        return True
    
    elif question.answer_type in ['text','textarea']:
        return valid_string(answer.answer)

    elif question.answer_type == 'email':
        return valid_email(answer.answer) and match(r'^\S+@\S+\.\S\S+$',
                                                    answer.answer)
    
    elif question.answer_type in ['select','radio']:
        return valid_select(answer.answer, question.answer_options)
    #
    else:
        return False
