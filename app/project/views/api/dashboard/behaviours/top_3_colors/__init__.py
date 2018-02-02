def get_top_3_colors(session) -> list:
    try:
        sql:str = 'SELECT answer, COUNT(*) AS most_popular ' +\
                  'FROM answers WHERE question_id = 8 ' +\
                  'GROUP BY answer ORDER BY most_popular DESC LIMIT 3'

        top3 = session.execute(sql)

        toreturn = []
        for t in top3:
            toreturn.append(t[0])

        return toreturn
    except Exception:
        return []
