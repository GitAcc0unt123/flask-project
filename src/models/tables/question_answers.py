from typing import List, TYPE_CHECKING

from sqlalchemy.sql import func

from src.models.database import db

if TYPE_CHECKING:
    from datetime import datetime


class QuestionAnswer(db.Model):
    __tablename__ = 'question_answers'

    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    question_id: int = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True)
    answer: List[str] = db.Column(db.ARRAY(db.String), nullable=False)
    time: 'datetime' = db.Column(db.DateTime, nullable=False, default=func.now())

    def __init__(self, user_id: int, question_id: int, answer: List[str]):
        self.user_id = user_id
        self.question_id = question_id
        self.answer = answer

    def update(self, new: dict) -> None:
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)
