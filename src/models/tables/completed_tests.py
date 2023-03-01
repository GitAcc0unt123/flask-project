from typing import TYPE_CHECKING

from sqlalchemy.sql import func

from src.models.database import db

if TYPE_CHECKING:
    from datetime import datetime


class CompletedTest(db.Model):
    __tablename__ = 'completed_tests'

    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    test_id: int = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete="CASCADE"), primary_key=True)
    complete_time: 'datetime' = db.Column(db.DateTime, nullable=False, default=func.now())

    def __init__(self, user_id: int, test_id: int):
        self.user_id = user_id
        self.test_id = test_id
