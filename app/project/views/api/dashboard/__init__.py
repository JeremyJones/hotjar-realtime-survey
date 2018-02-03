"""
"""

from apistar import http
from apistar.backends.sqlalchemy_backend import Session

from project.settings import SETTINGS
from project.utils.caches.memcache import mc

# dashboard data - 3 components
from .summary import get_summary
from .responses import get_responses
from .. import get_questions


def dashboard_data(data: http.RequestData, session: Session) -> dict:
    """
    API: Single call for a structure of data for the dashboard.
    """
    cachekey:str = 'dashboard_data_{survey}'.\
                   format(survey=SETTINGS['SURVEY_ID'])
    cached = mc.get(cachekey)

    if cached:
        try:
            if data['last'] == cached['responses']['_items_checksum']:
                return {"status":304}
            else:
                return cached
        except TypeError:
            pass
        
    dashdata:dict = {
        "questions": get_questions(session),
        "responses": get_responses(data, session),
        "summary": get_summary(session)
    }

    try:
        cache_time:int = SETTINGS['MEMCACHED_DASHBOARD_DATA']
    except KeyError:
        cache_time:int = 1
    finally:
        mc.set(cachekey, dashdata, cache_time)

    try:
        if data['last'] == dashdata['responses']['_items_checksum']:
            return {"status":304,"recached":True}
    except TypeError:
        pass
        
    return dashdata
