from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from tests.conftest import create_test, create_user
from src.models import Test

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from flask_sqlalchemy import SQLAlchemy


def test_route_test_get_all(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    create_test(app, db, 'title1', None,
                datetime(2000,1,11,0,0,0),
                datetime(2000,1,12,0,0,0))
    create_test(app, db, 'title2', 'description 123',
                datetime(2000,1,1,0,0,0),
                datetime(2000,1,12,0,0,0))

    response = client.get('/api/test')

    assert response.status_code == 200
    assert response.get_json() == [
        { 'id': 1, 'title': 'title1', 'description': '' },
        { 'id': 2, 'title': 'title2', 'description': 'description 123' }
    ]

def test_route_test_get(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    response = client.get('/api/test/1', headers=headers)

    assert response.status_code == 200
    assert response.get_json() == { 
        'id': 1,
        'title': 'title1',
        'description': '',
        'start': '2000-01-11T00:00:00',
        'end': '2000-01-12T00:00:00'
    }

def test_route_test_create(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    test_info = { 
        'title': 'title1',
        'start': '2000-01-12 00:00:00',
        'end': '2000-01-13 00:00:00'
    }

    response = client.post('/api/test', json=test_info, headers=headers)

    assert response.status_code == 201
    assert response.get_json() == { 'id': 1 }

    with app.app_context():
        test = db.get_or_404(Test, 1)
        assert test is not None
        assert test.id == 1
        assert test.title == test_info['title']
        assert test.description == ''
        assert test.start == datetime(2000, 1, 12, 0, 0)
        assert test.end == datetime(2000, 1, 13, 0, 0)

def test_route_test_update_title(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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
    
    update_test_info = { 
        'title': 'new title',
    }

    response = client.put('/api/test/1', json=update_test_info, headers=headers)

    assert response.status_code == 400

    with app.app_context():
        test = db.get_or_404(Test, 1)
        assert test is not None
        assert test.id == 1
        assert test.title == 'title1'
        assert test.description == 'description 11'
        assert test.start == datetime(2000, 1, 10, 0, 0)
        assert test.end == datetime(2000, 1, 11, 0, 0)

def test_route_test_update_time_bad_request(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    update_test_info = {
        'title': 'title1',
        'description': 'description 11',
        'start': datetime(2000,1,20,0,0,0),
        'end': datetime(2000,1,11,0,0,0)
    }

    response = client.put('/api/test/1', json=update_test_info, headers=headers)

    assert response.status_code == 400

    with app.app_context():
        test = db.get_or_404(Test, 1)
        assert test is not None
        assert test.id == 1
        assert test.title == 'title1'
        assert test.description == 'description 11'
        assert test.start == datetime(2000, 1, 10, 0, 0)
        assert test.end == datetime(2000, 1, 11, 0, 0)

def test_route_test_update_time(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    update_test_info = {
        'title': 'title1',
        'description': 'description 11',
        'start': '2010-01-10 00:00:00',
        'end': '2010-01-12 00:00:00'
    }

    response = client.put('/api/test/1', json=update_test_info, headers=headers)

    assert response.status_code == 200
    assert response.get_json() == {
        'id': 1,
        'title': 'title1',
        'description': 'description 11',
        'start': '2010-01-10T00:00:00',
        'end': '2010-01-12T00:00:00'
    }

    with app.app_context():
        test = db.get_or_404(Test, 1)
        assert test is not None
        assert test.id == 1
        assert test.title == 'title1'
        assert test.description == 'description 11'
        assert test.start == datetime(2010, 1, 10, 0, 0)
        assert test.end == datetime(2010, 1, 12, 0, 0)

def test_route_test_delete(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
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

    response = client.delete('/api/test/1', headers=headers)

    assert response.status_code == 204
    assert response.get_json() is None
    
    with app.app_context():
        tests = db.session.execute(select(Test).order_by(Test.id)).scalars().all()
        assert len(tests) == 1
        assert tests[0].id == 2
        assert tests[0].title == 'title2'
        assert tests[0].description == 'description 123'
        assert tests[0].start == datetime(2000, 1, 1, 0, 0)
        assert tests[0].end == datetime(2000, 1, 12, 0, 0)
