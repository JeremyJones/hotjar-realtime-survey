"""
settings class for the python developer task
"""

from apistar import environment, typesystem
from sqlalchemy.ext.declarative import declarative_base
from apistar.backends import sqlalchemy_backend

Base = declarative_base()


class Env(environment.Environment):
    """
    Subclassed environment for default & overridden variables.
    """
    properties = {
        'DEBUG': typesystem.boolean(default=False),
        'DATABASE_URL': typesystem.string(default='sqlite:///myexample.db')
    }

ENV = Env()

SETTINGS:dict = {
    'SURVEY_ID': 0,  # implement to run multiple
    #
    'MEMCACHED_DASHBOARD_DATA': 1,  # seconds
    'DASHBOARD_RESPONSES_LIMIT': 50,  # how many records, most recent
    #
    'DATABASE': {
        'URL': ENV['DATABASE_URL'],
        'METADATA': Base.metadata
    },
    'TEMPLATES': {'ROOT_DIR': 'templates',
                  'PACKAGE_DIRS': ['apistar']
                 },
    'STATICS': {'ROOT_DIR': 'lib',
                'PACKAGE_DIRS': ['apistar']
               }
}

commands = sqlalchemy_backend.commands
components = sqlalchemy_backend.components
