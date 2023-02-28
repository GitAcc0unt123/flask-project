from enum import Enum
from typing import List

from src.models.database import db


class AnswerTypeEnum(Enum):
    free_field = 'Свободный ответ'
    one_select = 'Выбор одного ответа'
    many_select = 'Выбор нескольких ответов'

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete="CASCADE"))
    text = db.Column(db.String(255), nullable=False)
    answer_type = db.Column(db.Enum(AnswerTypeEnum), nullable=False)
    show_answers = db.Column(db.ARRAY(db.String), nullable=False)
    true_answers = db.Column(db.ARRAY(db.String), nullable=False)

    test = db.relationship("Test", back_populates="questions")

    def __init__(self, test_id: int, text: str, answer_type: AnswerTypeEnum, show_answers: List[str], true_answers: List[str]):
        self.test_id = test_id
        self.text = text
        self.answer_type = answer_type
        self.show_answers = show_answers
        self.true_answers = true_answers

    def update(self, new: dict):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)
