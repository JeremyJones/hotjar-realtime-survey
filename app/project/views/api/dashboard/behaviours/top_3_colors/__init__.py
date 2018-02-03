def get_top_3_colors(session) -> list:
    try:
        sql:str = 'SELECT answer, COUNT(*) AS favourited ' +\
                  'FROM answers WHERE question_id = 8 ' +\
                  'GROUP BY answer ORDER BY favourited DESC LIMIT 3'

        top3 = session.execute(sql)

        toreturn = []
        for t in top3:
            toreturn.append(t[0])

        return toreturn
    except Exception:
        return []
