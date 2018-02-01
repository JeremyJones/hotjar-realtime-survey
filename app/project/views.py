"""
Views for Survey task
"""

from datetime import datetime as dt
from re import match
from hashlib import sha256
from random import SystemRandom

from apistar import http
from apistar import annotate
from apistar import render_template
from apistar.renderers import HTMLRenderer
from apistar.backends.sqlalchemy_backend import Session
from sqlalchemy import func

from werkzeug.http import dump_cookie
from werkzeug.http import parse_cookie
from project.settings import ENV

from project.models import Question
from project.models import Response
from project.models import Answer

from validate_email import validate_email


@annotate(renderers=[HTMLRenderer()])
def homepage() -> str:
    """
    Return the HTML for a home page placeholder.
    """
    datavars = {}
    return render_template('homepage.html', **datavars)


@annotate(renderers=[HTMLRenderer()])
def dashboard() -> str:
    """
    Return the HTML for the admin side management dashboard.
    """
    datavars = {}
    return render_template('dashboard/dashboard.html', **datavars)


@annotate(renderers=[HTMLRenderer()])
def survey() -> str:
    """
    Return the HTML for the survey.
    """
    datavars = {}
    return render_template('survey/survey.html', **datavars)


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


def get_questions(session: Session) -> dict:
    """
    API: Retrieve a list of the questions in JSON format
    """
    queryset = session.query(Question).\
               filter_by(survey_id = 0).\
               order_by(Question.order_in_list).\
               all()
    
    return {"_items": [{"question": question.question,
                        "required": question.required,
                        "id": question.id,
                        "answer_type": question.answer_type,
                        "answer_options": question.answer_options}
                       for question in queryset]
    }


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


def answer_question(data: http.RequestData, session: Session) -> dict:
    """
    API: POST an answer into the database, from an end-user
    """
    try:
        who = data['who']
        question_id = int(data['q'][15:])  # remove the 'answer2question' substring
        answer_val = data['a']
    except KeyError:
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
    answer.in_progress = 'N'  # required db field not implemented at this level.

    session.add(answer)
    session.commit()

    validAnswer = validate_answer(question, answer)
    
    return {"status":"OK", "validAnswer": validAnswer}


def get_responses(session: Session) -> dict:
    """
    API: Return the most recent 1000 responses, for the admin page.
    """
    return {"_items": [{"id": r.id, "started_at": r.started_at,
                        "is_completed": r.is_completed,
                        "answers": [{"question_id": a.question_id,
                                     "in_progress": a.in_progress,
                                     "answer": a.answer}
                                    for a in session.query(Answer).\
                                    filter_by(response_id = r.id).\
                                    all()]
                        }
                       for r in session.query(Response).\
                       order_by(Response.started_at.desc()).\
                       limit(1000).all()]
            }


def get_summary(session: Session) -> dict:
    """
    API: Get a JSON structure of summary data, for the admin page
    """

    try:  # https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query
        num_responses = session.query(func.count(Response.id)).first()[0]
    except Exception:
        num_responses = 0

    try:
        average_age = session.execute('SELECT AVG(CAST(answer AS TINYINT)) FROM answers ' +
                                      'WHERE question_id = %d' % 3).first()[0]
    except Exception:
        average_age = None
        
    gender_ratio = None
    top_3_colors = None
    last_updated = dt.now().isoformat()

    return {"updated_at": last_updated,
            "average_age": average_age,
            "top_3_colors": top_3_colors,
            "gender_ratio": gender_ratio,
            "num_responses": num_responses}
