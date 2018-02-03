from hashlib import sha256
from json import dumps

from project.models import Response, Answer
from project.settings import SETTINGS

def get_responses(data, session) -> dict:
    """
    API: Return the most recent non-empty responses, for the admin page.
    """
    items:list = [{"id": r.id, "started_at": r.started_at,
                   "is_completed": r.is_completed,
                   "answers": [{"question_id": a.question_id,
                                "in_progress": a.in_progress,
                                "answer": a.answer}
                               for a in session.query(Answer).\
                               filter_by(response_id = r.id).\
                               all()]}
                  for r in session.query(Response).\
                  order_by(Response.started_at.desc()).\
                  limit(100).all()]
    
    if 'SHOW_EMPTY_SURVEYS' in SETTINGS and \
       SETTINGS['SHOW_EMPTY_SURVEYS']:
        pass
    else:
        items:list = list(filter(lambda surv: len(surv['answers']) > 0,
                                 items))

    checksum:str = sha256(dumps(items).encode('utf-8')).hexdigest()

    try:
        if data['checksum'] == checksum:
            return {}
    except(TypeError, KeyError):
        pass

    # add a count of all of them
    try:
        surveys_count:int = int(session.\
                                execute('SELECT COUNT(DISTINCT(response_id)) ' + \
                                        'FROM answers WHERE survey_id = %d ' %
                                        SETTINGS['SURVEY_ID']).first()[0])
    except Exception:
        surveys_count:int = 0
    
    return {"_items": items, "_items_count": len(items),
            "_items_checksum": checksum, "count": surveys_count}