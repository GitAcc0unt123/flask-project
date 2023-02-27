from sqlalchemy.sql import func

from src.models.database import db


class CompletedTest(db.Model):
    __tablename__ = 'completed_tests'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete="CASCADE"), primary_key=True)
    complete_time = db.Column(db.DateTime, nullable=False, default=func.now())

    def __init__(self, user_id: int, test_id: int):
        self.user_id = user_id
        self.test_id = test_id

    # __table_args__ = (
    #     PrimaryKeyConstraint(field2, field1),
    #     {},
    # )