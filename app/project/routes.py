from apistar import Include, Route
from project.views import hello, hi
from apistar.handlers import docs_urls, static_urls

routes = [
    Route('/', 'GET', hello),
    Route('/hi', 'GET', hi),

    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
