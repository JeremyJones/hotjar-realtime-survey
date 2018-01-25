from apistar.frameworks.wsgi import WSGIApp as App
from project.routes import routes
from project.settings import settings


app = App(routes=routes, settings=settings)


if __name__ == '__main__':
    app.main()
