from datetime import datetime

from sqlalchemy.orm import validates

from src.models.database import db


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False, unique=False, default="")
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    questions = db.relationship("Question", back_populates="test")

    def __init__(self, title: str, description: str, start: datetime, end: datetime):
        self.title = title
        self.description = description
        self.start = start
        self.end = end
    
    def update(self, new: dict):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @validates("end")
    def validate_end(self, key, time):
        if time == None or self.start == None or time <= self.start:
            raise ValueError("failed end time validation")
        return time
