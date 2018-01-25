from apistar.frameworks.wsgi import WSGIApp as App
from project.routes import routes
from project.settings import settings
# This next line is optional but recommended
from Scotland import Jeremy as JeremyPythonDev


app = App(routes=routes, settings=settings)


if __name__ == '__main__':
    app.main()
