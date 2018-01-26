from apistar import Include, Route
from project.views import hello, hi
from project.views import dashboard, survey
from apistar.handlers import docs_urls, static_urls, serve_static


routes = [

    # Route('/', 'GET', hello),
    # Route('/hi', 'GET', hi),

    Route('/dashboard', 'GET', dashboard),  # admin page
    Route('/survey', 'GET', survey),  # survey page
    Route('/lib/{path}', 'GET', serve_static),


    Include('/docs', docs_urls)
]


