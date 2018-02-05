class genderRatioBehaviour():

    gender_question_id = 6  #

    def __init__(self, question_id=None) -> None:
        self.question_id = question_id = self.gender_question_id

    def get_question_id(self) -> int:
        return self.question_id
    
    def getResult(self, session) -> dict:
        sql = 'SELECT answer, COUNT(*) FROM answers ' +\
              'WHERE question_id = %d ' % self.get_question_id() +\
              'AND answer != "Please select" ' +\
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
            #raise
            return {}
