"""
URL Routing for Survey task
"""
from apistar import Route, Include

from apistar.handlers import docs_urls
from apistar.handlers import serve_static

from project.views.html import survey, dashboard
from project.views.html import homepage

from project.views.auth import get_identifier

from project.views.api import get_questions
from project.views.api.survey import answer_question
from project.views.api.dashboard import get_summary, get_responses


ROUTES = [

    # HTML pages & static URLs
    Route('/dashboard', 'GET', dashboard),  # admin page
    Route('/survey', 'GET', survey),  # survey page
    Route('/lib/{path}', 'GET', serve_static),  # static css & js
    Route('/', 'GET', homepage), # solution homepage (list of links)

    # API URLs
    Route('/getIdentifier', 'POST', get_identifier),
    Route('/questions', 'POST', get_questions),
    # 
    Route('/answer', 'POST', answer_question),
    #
    Route('/summary', 'POST', get_summary),
    Route('/responses', 'POST', get_responses),
    
    # Others
    Include('/docs', docs_urls)  # built-in admin ui
]
