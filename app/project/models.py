from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, default=0)
    order_in_list = Column(Integer, default=1)
    required = Column()
    question = Column(String)
    answer_type = Column(String)
    answer_options = Column(String)
    

class Response(Base):
    __tablename__ = 'responses'
    
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, nullable=False, default=0)
    started_at = Column(Integer, nullable=False)
    is_completed = Column()
    

class Answer(Base):
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer)
    question_id = Column(String)
    in_progress = Column()

    answer = Column(String)
