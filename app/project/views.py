"""
Views for Survey task
"""

from project.handlers.html import survey, dashboard
from project.handlers.html import homepage

from project.handlers.auth import get_identifier
from project.handlers.api import get_questions

from project.handlers.api.survey import answer_question
from project.handlers.api.dashboard import get_summary, get_responses
