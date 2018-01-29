"""Python Developer Task
=====================
Jeremy Jones, February 2018
---------------------------

### Synopsis

    $ apistar run

Open browsers to
     /dashboard for the management dashboard
     /survey for the end-user survey
"""


from apistar.frameworks.wsgi import WSGIApp as App

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from apistar.backends import sqlalchemy_backend

from project.routes import ROUTES
from project.settings import SETTINGS, COMMANDS, COMPONENTS


# This next line is optional but recommended
from Scotland import JerJones as JeremyPythonDev

"""
Base = declarative_base


class SurveyRespondent(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
"""


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
