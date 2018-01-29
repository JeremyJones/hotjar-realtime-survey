"""
Views for Survey task
"""

from apistar import render_template, annotate
from apistar.renderers import HTMLRenderer
from apistar.backends.sqlalchemy_backend import Session

from project.models import Question
from project.models import Response
from project.models import Answer

#from project.settings import SETTINGS


@annotate(renderers=[HTMLRenderer()])
def dashboard() -> str:
    """
    Return the HTML for the admin side management dashboard.
    """
    datavars = {}
    # return "Hello. My env looks like this: {}".format(SETTINGS)

    return render_template('dashboard/dashboard.html', **datavars)


@annotate(renderers=[HTMLRenderer()])
def survey() -> str:
    """
    Return the HTML for the survey.
    """
    return render_template('survey/survey.html')



def get_questions(session: Session) -> dict:
    """
    API: Retrieve a JSON list of the questions
    """
    queryset = session.query(Question).all()
    
    return {"_items": [{'id': q.id, 'question': q.question}
                       for q in queryset]}


def answer_question(session: Session) -> dict:
    """
    API: POST an answer into the database
    """
    return {}


def get_responses(session: Session) -> dict:
    """
    API: Get a list of responses, for the admin page
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
    average_age = None
    gender_ratio = None
    top_3_colors = None

    # figure out each of those

    return {"average_age": average_age}
    
