from apistar import environment, typesystem


class Env(environment.Environment):
    properties = {
        'DEBUG': typesystem.boolean(default=False),
        'DATABASE_URL': typesystem.string(default='sqlite://')
    }

env = Env()

settings = {
    'DATABASE': {
        'URL': env['DATABASE_URL']
    },
    'TEMPLATES': {'ROOT_DIR': 'templates',
                  'PACKAGE_DIRS': ['apistar']
    },
    'STATICS': {'ROOT_DIR': 'lib',
                'PACKAGE_DIRS': ['apistar']
    }
}