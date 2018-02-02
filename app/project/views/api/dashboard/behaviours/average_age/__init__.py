def get_average_age(session) -> float:
    try:
        return float(session.execute('SELECT AVG(CAST(answer AS UNSIGNED)) FROM answers ' +
                                     'WHERE question_id = %d' % 3).first()[0])
    except Exception:
        return None
