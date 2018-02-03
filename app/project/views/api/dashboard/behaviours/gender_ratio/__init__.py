def get_gender_ratio(session) -> dict:
    sql = 'SELECT answer, COUNT(*) FROM answers ' +\
          'WHERE question_id = %d ' % 6 +\
          'GROUP BY answer LIMIT 2'

    try:
        result = session.execute(sql)
        rows = []
        for row in result:
            rows.append(row)

        nums = {}
        total = 0
        ratios = {}

        for r in rows:
            nums[r[0]] = r[1]
            total += r[1]

        for r in rows:
            ratios[r[0]] = {'pct': '%d%%' % ((r[1]/ (total or 1)) * 100),
                            'cnt': nums[r[0]]}

        return ratios

    except Exception:
        raise
        return {}
