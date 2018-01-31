"""
Views for Survey task
"""

from datetime import datetime as dt

from apistar import render_template, annotate
from apistar.renderers import HTMLRenderer
from apistar.backends.sqlalchemy_backend import Session
from sqlalchemy import func

from project.models import Question
from project.models import Response
from project.models import Answer


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
    return {"eui": "abcdefghijklmnop",
            "scr": 1}


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


def answer_question(session: Session) -> dict:
    """
    API: POST an answer into the database, from an end-user
    """
    return {}


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
