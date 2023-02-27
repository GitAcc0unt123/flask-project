from datetime import datetime

from sqlalchemy import select, and_

from tests.conftest import create_test, create_user, create_completed_test
from src.models import CompletedTest


def test_route_complete_test(client, app, db):
    # sign in
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

    completed_test_info = { 
        'test_id': 1,
    }
    response = client.post('/api/completed-test', json=completed_test_info, headers=headers)

    assert response.status_code == 201
    assert response.get_json() == None

    with app.app_context():
        stmt = select(CompletedTest).where(and_(CompletedTest.user_id==1, CompletedTest.test_id==1))
        completed_test = db.session.execute(stmt).scalar_one_or_none()
        assert completed_test != None
        assert completed_test.user_id == 1
        assert completed_test.test_id == 1
        assert completed_test.complete_time != None


def test_route_complete_test_exist(client, app, db):
    # sign in
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
    create_completed_test(app, db, 1, 1)

    with app.app_context():
        stmt = select(CompletedTest).where(and_(CompletedTest.user_id==1, CompletedTest.test_id==1))
        completed_test = db.session.execute(stmt).scalar_one_or_none()
        assert completed_test != None
        assert completed_test.user_id == 1
        assert completed_test.test_id == 1
        assert completed_test.complete_time != None

    completed_test_info = { 
        'test_id': 1,
    }
    response = client.post('/api/completed-test', json=completed_test_info, headers=headers)

    assert response.status_code == 201
    assert response.get_json() == None

    with app.app_context():
        stmt = select(CompletedTest).where(and_(CompletedTest.user_id==1, CompletedTest.test_id==1))
        completed_test_after_request = db.session.execute(stmt).scalar_one_or_none()
        assert completed_test.user_id == completed_test_after_request.user_id
        assert completed_test.test_id == completed_test_after_request.test_id
        assert completed_test.complete_time == completed_test_after_request.complete_time
