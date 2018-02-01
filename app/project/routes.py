"""
URL Routing for Survey task
"""
from apistar import Route
from apistar import Include

from apistar.handlers import docs_urls
from apistar.handlers import serve_static

from project.views.html import survey, dashboard
from project.views.html import homepage

from project.views.auth import get_identifier

from project.views.api import get_questions
from project.views.api.survey import answer_question
from project.views.api.dashboard import get_summary, get_responses


ROUTES = [

    Route('/', 'GET', homepage),

    # HTML pages & static URLs
    Route('/dashboard', 'GET', dashboard),  # admin page
    Route('/survey', 'GET', survey),  # survey page
    Route('/lib/{path}', 'GET', serve_static),

    # API URLs
    Route('/questions', 'POST', get_questions),
    Route('/responses', 'POST', get_responses),
    Route('/summary', 'POST', get_summary),
    Route('/answer', 'POST', answer_question),
    Route('/getIdentifier', 'POST', get_identifier),
    
    # Others
    Include('/docs', docs_urls)  # built-in admin ui
]
