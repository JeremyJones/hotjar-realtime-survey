"""
Helpful utilities, and also plug-in functionality.
"""

from project.models import Question
from project.models import Answer

from validate_email import validate_email

def validate_answer(question: Question, answer: Answer) -> bool:
    """Given a Question and Answer object, return True/False if the
    answer given is a valid answer according to that question's
    validation rules (e.g. email etc.).
    """
    if question.answer_type == 'text':
        return bool(question.required == 'n' or len(answer.answer) > 0)
    elif question.answer_type == 'email':
        return bool(validate_email(answer.answer))
    else:
        return False

