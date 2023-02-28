from datetime import datetime
from typing import List

import pytest

from src import create_flask_app
from src.utils.config import Config
from src.models import db as test_db
from src.models import User, Test, Question, QuestionAnswer, AnswerTypeEnum, CompletedTest


@pytest.fixture(scope="session")
def app():
    print('app')
    config = Config('config.yaml', '.env')
    config.flask['SQLALCHEMY_DATABASE_URI'] = config.flask['SQLALCHEMY_TEST_DATABASE_URI']
    config.flask['TESTING'] = True
    app = create_flask_app(config.flask)
    yield app


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        test_db.drop_all()
        test_db.create_all()
    return test_db


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


def create_user(app, db,
                     username: str ='username123',
                     password: str ='password123',
                     name: str ='name example',
                     email: str ='example@mail.com'
) -> None:
    print('create_user')
    with app.app_context():
        user = User(username, password, name, email)
        db.session.add(user)
        db.session.commit()


def create_test(app, db, 
                title: str, 
                description: str, 
                start: datetime, 
                end: datetime
) -> None:
    print('create_test')
    with app.app_context():
        test = Test(title, description, start, end)
        db.session.add(test)
        db.session.commit()


def create_question(app, db,
                    test_id: int,
                    text: str,
                    answer_type: AnswerTypeEnum,
                    show_answers: List[str],
                    true_answers: List[str]
) -> None:
    print('create_question')
    with app.app_context():
        question = Question(test_id, text, answer_type, show_answers, true_answers)
        db.session.add(question)
        db.session.commit()


def create_question_answer(app, db, 
                           user_id: int,
                           question_id: int,
                           answer: List[str]
) -> None:
    print('create_question_answer')
    with app.app_context():
        question_answer = QuestionAnswer(user_id, question_id, answer)
        db.session.add(question_answer)
        db.session.commit()


def create_completed_test(app, db, user_id: int, test_id: int) -> None:
    print('create_completed_test')
    with app.app_context():
        completed_test = CompletedTest(user_id, test_id)
        db.session.add(completed_test)
        db.session.commit()
