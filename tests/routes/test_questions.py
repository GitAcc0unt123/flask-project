from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from tests.conftest import create_test, create_user, create_question, create_completed_test
from src.models import Question, AnswerTypeEnum

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from flask_sqlalchemy import SQLAlchemy


def test_route_question_get_test_doesnt_exist(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])

    response = client.get('/api/tests/10/questions', headers=headers)

    assert response.status_code == 404
    #assert response.get_json() == None

def test_route_question_get_uncompleted_test(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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
    create_question(app, db, 2, 'question text3',
                AnswerTypeEnum.many_select,
                ['1', '2', '4'],
                ['2', '4'])

    response = client.get('/api/tests/1/questions', headers=headers)

    assert response.status_code == 200
    assert response.get_json() == [
        { 'id': 1, 'test_id': 1, 'text': 'question text1', 'answer_type': 'free_field', 'show_answers': []},
        { 'id': 2, 'test_id': 1, 'text': 'question text2', 'answer_type': 'one_select', 'show_answers': ['1', '2', '3'] }
    ]

def test_route_question_get_completed_test(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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
    create_question(app, db, 2, 'question text3',
                AnswerTypeEnum.many_select,
                ['1', '2', '4'],
                ['2', '4'])
    create_completed_test(app, db, 1, 1)

    response = client.get('/api/tests/1/questions', headers=headers)

    assert response.status_code == 200
    assert response.get_json() == [
        {
            'id': 1,
            'test_id': 1,
            'text': 'question text1',
            'answer_type': 'free_field',
            'show_answers': [],
            'true_answers': ['1703']
        },
        {
            'id': 2,
            'test_id': 1,
            'text': 'question text2',
            'answer_type': 'one_select',
            'show_answers': ['1', '2', '3'],
            'true_answers': ['3']
        }
    ]

def test_route_question_get(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])

    create_question(app, db, 1, 'question text2',
                AnswerTypeEnum.one_select,
                ['1', '2', '3'],
                ['3'])

    response = client.get('/api/tests/1/questions/2', headers=headers)

    assert response.status_code == 200
    assert response.get_json() == {
        'id': 2,
        'test_id': 1,
        'text': 'question text2',
        'answer_type': AnswerTypeEnum.one_select.name,
        'show_answers': ['1', '2', '3']
    }

def test_route_question_create_test_doesnt_exist(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    question_info = {
        'text': 'question text2',
        'answer_type': AnswerTypeEnum.one_select.name,
        'show_answers': ['1', '2', '3'],
        'true_answers': ['3']
    }
    response = client.post('/api/tests/10/questions', json=question_info, headers=headers)
    assert response.status_code == 404

def test_route_question_create(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    question_info = {
        'text': 'question text2',
        'answer_type': AnswerTypeEnum.one_select.name,
        'show_answers': ['1', '2', '3'],
        'true_answers': ['3']
    }
    response = client.post('/api/tests/1/questions', json=question_info, headers=headers)

    assert response.status_code == 201
    assert response.get_json() == { 'id': 1 }

    with app.app_context():
        question = db.get_or_404(Question, 1)
        assert question is not None
        assert question.id == 1
        assert question.test_id == 1
        assert question.text == question_info['text']
        assert question.answer_type == AnswerTypeEnum.one_select
        assert question.show_answers == question_info['show_answers']
        assert question.true_answers == question_info['true_answers']

def test_route_question_update_text(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    create_test(app, db, 'title1', 'description 11',
                datetime(2000,1,10,0,0,0),
                datetime(2000,1,11,0,0,0))
    
    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])
    
    update_question_info = {
        'text': 'new question text',
        'answer_type': AnswerTypeEnum.free_field.name,
        'show_answers': [],
        'true_answers': ['1703']
    }

    response = client.put('/api/tests/1/questions/1', json=update_question_info, headers=headers)

    assert response.status_code == 200
    assert response.get_json() == update_question_info | {'id':1, 'test_id': 1}

    with app.app_context():
        question = db.get_or_404(Question, 1)
        assert question is not None
        assert question.id == 1
        assert question.test_id == 1
        assert question.text == update_question_info['text']
        assert question.answer_type.name == update_question_info['answer_type']
        assert question.show_answers == update_question_info['show_answers']
        assert question.true_answers == update_question_info['true_answers']

def test_route_question_update_answer_bad_request(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    create_test(app, db, 'title1', 'description 11',
                datetime(2000,1,10,0,0,0),
                datetime(2000,1,11,0,0,0))

    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])

    update_question_info = {
        'text': 'new description',
        'answer_type': AnswerTypeEnum.one_select.name
    }

    response = client.put('/api/tests/1/questions/1', json=update_question_info, headers=headers)

    assert response.status_code == 400

    with app.app_context():
        question = db.get_or_404(Question, 1)
        assert question is not None
        assert question.id == 1
        assert question.test_id == 1
        assert question.text == 'question text1'
        assert question.answer_type == AnswerTypeEnum.free_field
        assert question.show_answers == []
        assert question.true_answers == ['1703']

def test_route_question_update_answer(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    create_test(app, db, 'title1', 'description 11',
                datetime(2000,1,10,0,0,0),
                datetime(2000,1,11,0,0,0))

    create_question(app, db, 1, 'question text1',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])

    update_question_info = {
        'text': 'new description',
        'answer_type': AnswerTypeEnum.one_select.name,
        'show_answers': ['2014', '2015', '2016'],
        'true_answers': ['2016']
    }

    response = client.put('/api/tests/1/questions/1', json=update_question_info, headers=headers)

    assert response.status_code == 200
    assert response.get_json() == update_question_info | {'id': 1, 'test_id': 1}

    with app.app_context():
        question = db.get_or_404(Question, 1)
        assert question is not None
        assert question.id == 1
        assert question.test_id == 1
        assert question.text == update_question_info['text']
        assert question.answer_type == AnswerTypeEnum.one_select
        assert question.show_answers == update_question_info['show_answers']
        assert question.true_answers == update_question_info['true_answers']

def test_route_question_delete(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    create_question(app, db, 1, 'question text',
                AnswerTypeEnum.free_field,
                [],
                ['1703'])

    response = client.delete('/api/tests/1/questions/1', headers=headers)

    assert response.status_code == 204
    assert response.get_json() is None
    
    with app.app_context():
        questions = db.session.execute(select(Question).order_by(Question.id)).scalars().all()
        assert len(questions) == 0
