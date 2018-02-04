class averageAgeBehaviour():

    default_question_id = 3  #
    
    def __init__(self, question_id=None) -> None:
        self.question_id = question_id or self.default_question_id

    def get_question_id(self) -> int:
        return self.question_id

    def getResult(self, session) -> float:
        """Raw SQL query passed into the database with hard-coded question
        id. Of all the relevant answers, cast all of them to integers and then
        calculate the average.
        """
        try:
            return float(session.execute('SELECT AVG(CAST(answer AS UNSIGNED)) ' +
                                         'FROM answers ' +
                                         'WHERE question_id = %d' % \
                                         self.get_question_id()).\
                         first()[0])
        except Exception:
            return 0.0
