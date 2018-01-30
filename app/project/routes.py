"""
URL Routing for Survey task
"""
from apistar import Route

# these next ones are for apistar's built-in admin/docs interface
from apistar import Include
from apistar.handlers import docs_urls

#from project.views import hello, hi  # hello worlds
from apistar.handlers import serve_static
from project.views import dashboard
from project.views import survey

from project.views import get_questions
from project.views import get_responses
from project.views import get_summary
from project.views import answer_question


ROUTES = [

    # Route('/', 'GET', hello),
    # Route('/hi', 'GET', hi),

    # HTML pages & static URLs
    Route('/dashboard', 'GET', dashboard),  # admin page
    Route('/survey', 'GET', survey),  # survey page
    Route('/lib/{path}', 'GET', serve_static),

    # API URLs
    Route('/questions', 'GET', get_questions),
    Route('/responses', 'GET', get_responses),
    Route('/summary', 'GET', get_summary),
    Route('/answer', 'POST', answer_question),
    
    # Others
    Include('/docs', docs_urls)  # built-in admin ui
]