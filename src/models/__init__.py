from src.models.tables import User, Test, CompletedTest, Question, QuestionAnswer, AnswerTypeEnum
from src.models.database import db

# It is a list of strings defining what symbols in a module will be exported when from <module> import * is used on the module
__all__ = [
    db,
    User,
    Test,
    CompletedTest,
    Question,
    QuestionAnswer,
    AnswerTypeEnum
]