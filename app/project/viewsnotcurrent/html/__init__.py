"""
Group of handlers for server-generated HTML pages.
"""

from apistar import annotate
from apistar import render_template
from apistar.renderers import HTMLRenderer


@annotate(renderers=[HTMLRenderer()])
def homepage() -> str:
    """
    Return the HTML for a home page (convenience page of project links).
    """
    datavars = {}
    return render_template('homepage.html', **datavars)


@annotate(renderers=[HTMLRenderer()])
def survey() -> str:
    """
    Return the HTML for the survey.
    """
    datavars = {}
    return render_template('survey/survey.html', **datavars)


@annotate(renderers=[HTMLRenderer()])
def dashboard() -> str:
    """
    Return the HTML for the admin side management dashboard.
    """
    datavars = {}
    return render_template('dashboard/dashboard.html', **datavars)
