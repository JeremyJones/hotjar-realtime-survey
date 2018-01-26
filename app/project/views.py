"""
Views for Survey task
"""

from apistar import render_template, annotate
from apistar.renderers import HTMLRenderer


@annotate(renderers=[HTMLRenderer()])
def dashboard() -> str:
    """
    Return the HTML for the admin side management dashboard.
    """
    datavars = {}
    return render_template('dashboard/dashboard.html', **datavars)


@annotate(renderers=[HTMLRenderer()])
def survey() -> str:
    """
    Return the HTML for the survey.
    """
    return render_template('survey/survey.html')
