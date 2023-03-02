from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select, and_

from tests.conftest import create_test, create_user, create_question, create_question_answer
from src.models import QuestionAnswer, AnswerTypeEnum

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from flask_sqlalchemy import SQLAlchemy


def test_route_get_question_answers(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    create_user(app, db)
    credentials = {
        'username': 'username123',
        'password': 'password123'
    }
    response = client.post('/api/auth/sign-in', json=credentials)
    token = response.get_json()['access_token']
    headers = {
        'cookie': f'access_token={token}'
    }

    create_test(app, db, 'title1', None,
                datetime(2000,1,11,0,0,0),
                datetime(2000,1,12,0,0,0))
    create_test(app, db, 'title2', 'description 123',
                datetime(2000,1,1,0,0,0),
                datetime(2000,1,12,0,0,0))

    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])
    create_question(app, db, 1, 'question text2',
                AnswerTypeEnum.one_select,
                ['1', '2', '3'],
                ['3'])
    create_question(app, db, 1, 'question text3',
                AnswerTypeEnum.many_select,
                ['1', '2', '4'],
                ['2', '4'])
    
    create_question_answer(app, db, 1, 1, ['1703'])
    create_question_answer(app, db, 1, 3, ['1', '2'])

    response = client.get('/api/question-answer?test_id=1', headers=headers)

    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json[0]['user_id'] == 1
    assert response_json[0]['question_id'] == 1
    assert response_json[0]['answer'] == ['1703']
    assert response_json[1]['user_id'] == 1
    assert response_json[1]['question_id'] == 3
    assert response_json[1]['answer'] == ['1', '2']

def test_route_question_answers_CREATE_or_update(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    create_user(app, db)
    credentials = {
        'username': 'username123',
        'password': 'password123'
    }
    response = client.post('/api/auth/sign-in', json=credentials)
    token = response.get_json()['access_token']
    headers = {
        'cookie': f'access_token={token}'
    }

    create_test(app, db, 'title1', None,
                datetime(2000,1,10,0,0,0),
                datetime(2000,1,11,0,0,0))
    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])

    question_answer_info = { 
        'question_id': 1,
        'answer': ['1703']
    }
    response = client.post('/api/question-answer', json=question_answer_info, headers=headers)

    assert response.status_code == 201
    assert response.get_json() is None
    with app.app_context():
        stmt = select(QuestionAnswer).where(and_(QuestionAnswer.user_id==1, QuestionAnswer.question_id==1))
        question_answer = db.session.execute(stmt).scalar_one_or_none()
        assert question_answer is not None
        assert question_answer.user_id == 1
        assert question_answer.question_id == 1
        assert question_answer.answer == ['1703']

def test_route_question_answers_create_or_UPDATE(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    create_user(app, db)
    credentials = {
        'username': 'username123',
        'password': 'password123'
    }
    response = client.post('/api/auth/sign-in', json=credentials)
    token = response.get_json()['access_token']
    headers = {
        'cookie': f'access_token={token}'
    }

    create_test(app, db, 'title1', None,
                datetime(2000,1,10,0,0,0),
                datetime(2000,1,11,0,0,0))
    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])
    create_question_answer(app, db, 1, 1, ['1701'])
    with app.app_context():
        stmt = select(QuestionAnswer).where(and_(QuestionAnswer.user_id==1, QuestionAnswer.question_id==1))
        question_answer = db.session.execute(stmt).scalar_one_or_none()
        assert question_answer is not None
        assert question_answer.user_id == 1
        assert question_answer.question_id == 1
        assert question_answer.answer == ['1701']

    question_answer_info = { 
        'question_id': 1,
        'answer': ['1703']
    }
    response = client.post('/api/question-answer', json=question_answer_info, headers=headers)

    assert response.status_code == 201
    assert response.get_json() is None

    with app.app_context():
        stmt = select(QuestionAnswer).where(and_(QuestionAnswer.user_id==1, QuestionAnswer.question_id==1))
        question_answer = db.session.execute(stmt).scalar_one_or_none()
        assert question_answer is not None
        assert question_answer.user_id == 1
        assert question_answer.question_id == 1
        assert question_answer.answer == ['1703']
