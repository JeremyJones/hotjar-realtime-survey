from apistar import Include, Route
from project.views import hello, hi
from apistar.handlers import docs_urls, static_urls, serve_static


routes = [
    Route('/', 'GET', hello),
    Route('/hi', 'GET', hi),


    #Route('/dashboard', 'GET', hello),  # admin side
    #Route('/survey', 'GET', hello),  # survey side
    Route('/lib/{path}', 'GET', serve_static),


    Include('/docs', docs_urls)
]
