"""
URL Routing for Survey task
"""
from apistar import Route, Include

from apistar.handlers import docs_urls
from apistar.handlers import serve_static

from project.views.html import survey
from project.views.html import dashboard
from project.views.html import homepage

from project.views.auth import get_identifier

from project.views.api import get_questions
from project.views.api.survey.answer import answer_question
from project.views.api.survey.finalise import finalise
from project.views.api.survey.getState import get_state
from project.views.api.dashboard import dashboard_data


routes:list = [

    # HTML pages & static URLs
    Route('/dashboard', 'GET', dashboard),  # admin page
    Route('/survey', 'GET', survey),  # survey page
    Route('/lib/{path}', 'GET', serve_static),  # static files
    Route('/', 'GET', homepage), # solution homepage (list of links)

    # API URLs
    Route('/getIdentifier', 'POST', get_identifier),
    Route('/questions', 'POST', get_questions),
    # 
    Route('/answer', 'POST', answer_question),
    Route('/finalise', 'POST', finalise),
    Route('/getState', 'POST', get_state),
    #
    Route('/dashdata', 'POST', dashboard_data),
    
    # Others
    Include('/docs', docs_urls)  # built-in admin ui
]
