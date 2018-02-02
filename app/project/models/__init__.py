from datetime import datetime as dt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, default=0)
    order_in_list = Column(Integer, default=1)
    required = Column()
    allow_multiple = Column()
    question = Column(String)
    answer_type = Column(String)
    answer_options = Column(String)
    

class Response(Base):
    __tablename__ = 'responses'
    
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, nullable=False, default=0)
    end_user_id = Column(String)
    end_user_ip = Column(String, default="")
    started_at = Column(Integer, nullable=False)
    last_at = Column(Integer)
    is_completed = Column()

    def __init__(self):
        self.last_at = int(dt.now().timestamp())


class Answer(Base):
    __tablename__ = 'answers'
    
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer)
    response_id = Column(Integer)
    question_id = Column(String)
    in_progress = Column()
    valid_answer = Column()
    answered_at = Column(Integer)

    answer = Column(String)
