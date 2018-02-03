from datetime import datetime as dt

from apistar import http
from apistar.backends.sqlalchemy_backend import Session

from project.models import Question, Response, Answer

def get_state(data: http.RequestData, session: Session) -> dict:
    return {}
