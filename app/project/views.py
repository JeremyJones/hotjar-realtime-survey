from apistar import render_template, annotate
from apistar.renderers import HTMLRenderer


@annotate(renderers=[HTMLRenderer()])
def hi() -> str:
    """
    Test of template processing.
    """
    datavars = {}
    return render_template('hieverybody.html', **datavars)


def hello(username:str=None) -> dict:
    """
    Basic hello message to confirm proxying, function etc.
    """

    message = 'Welcome to the future, {who}!'
    return {'message': message.format(who=username or 'mystery person')}

