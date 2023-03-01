from typing import TYPE_CHECKING

from sqlalchemy.orm import validates

from src.models.database import db

if TYPE_CHECKING:
    from datetime import datetime


class Test(db.Model):
    __tablename__ = 'tests'

    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(255), nullable=False, unique=True)
    description: str = db.Column(db.Text, nullable=False, unique=False, default="")
    start: 'datetime' = db.Column(db.DateTime, nullable=False)
    end: 'datetime' = db.Column(db.DateTime, nullable=False)

    questions = db.relationship("Question", back_populates="test")

    def __init__(self, title: str, description: str, start: 'datetime', end: 'datetime'):
        self.title = title
        self.description = description
        self.start = start
        self.end = end
    
    def update(self, new: dict) -> None:
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @validates("end")
    def validate_end(self, key, time):
        if time is None or self.start is None or time <= self.start:
            raise ValueError("failed end time validation")
        return time
