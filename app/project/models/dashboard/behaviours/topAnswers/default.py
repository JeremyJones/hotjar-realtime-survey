class topAnswersBehaviour():

    default_question_id = 8  #
    default_limit = 3
    
    def __init__(self, question_id=None, limit=None) -> None:
        self.question_id:int = question_id or self.default_question_id
        self.limit:int = limit or self.default_limit

    def get_question_id(self) -> int:
        return self.question_id

    def get_limit(self) -> int:
        return self.limit

    def getResult(self, session) -> list:
        try:
            sql:str = 'SELECT answer, COUNT(*) AS favourited ' +\
                      'FROM answers ' +\
                      'WHERE question_id = %d ' % self.get_question_id() +\
                      'GROUP BY answer ORDER BY favourited DESC ' +\
                      'LIMIT %d' % self.get_limit()
            
            tops = session.execute(sql)
            favs:list = []
            
            for t in tops:
                favs.append("{answer} ({count:,})".format(answer=t[0],
                                                          count=t[1]))

            return favs
        except Exception:
            return []

        
class topColoursBehaviour(topAnswersBehaviour):
    pass
