"""Python Developer Task
=====================
Jeremy Jones, February 2018
---------------------------
"""

from apistar.frameworks.wsgi import WSGIApp as App

from project.settings import SETTINGS
from project.settings import commands
from project.settings import components
from project.routes import routes


app = App(routes=routes, settings=SETTINGS,
          commands=commands, components=components)


@staticmethod
def main() -> None:
    """
    Run the main application server.
    """
    app.main()


if __name__ == '__main__':
    main()
