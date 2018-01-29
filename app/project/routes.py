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


ROUTES = [

    # Route('/', 'GET', hello),
    # Route('/hi', 'GET', hi),

    Route('/dashboard', 'GET', dashboard),  # admin page
    Route('/survey', 'GET', survey),  # survey page
    Route('/lib/{path}', 'GET', serve_static),

    Include('/docs', docs_urls)  # built-in admin ui
]
