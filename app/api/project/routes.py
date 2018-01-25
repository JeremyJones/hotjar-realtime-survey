from apistar import Include, Route
from project.views import hello
from apistar.handlers import docs_urls, static_urls

routes = [
    Route('/', 'GET', hello),

    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
