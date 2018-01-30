"""Python Developer Task
=====================
Jeremy Jones, February 2018
---------------------------
"""


from apistar.frameworks.wsgi import WSGIApp as App

from project.settings import SETTINGS
from project.settings import COMMANDS
from project.settings import COMPONENTS
from project.routes import ROUTES


app = App(routes=ROUTES, settings=SETTINGS,
          commands=COMMANDS, components=COMPONENTS)


@staticmethod
def main() -> None:
    """
    Run the main application server.
    """
    app.main()


if __name__ == '__main__':
    main()
