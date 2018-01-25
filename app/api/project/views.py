def hello(username=None) -> dict:
    """
    Basic hello message to confirm proxying, function etc.
    """

    message = 'Welcome to the future, {who}!'
    return {'message': message.format(who=username or 'mystery person')}
