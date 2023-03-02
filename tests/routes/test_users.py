from typing import TYPE_CHECKING

from tests.conftest import create_user
from src.models import User

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from flask_sqlalchemy import SQLAlchemy


def test_route_auth_sign_up(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    user_info = {
        'username': 'username123',
        'password': 'password123',
        'name': 'name example',
        'email': 'example@mail.com'
    }

    response = client.post('/api/auth/sign-up', json=user_info)
    assert response.status_code == 201
    assert response.get_json() == {"id": 1}

    with app.app_context():
        user = db.get_or_404(User, 1)
        assert user is not None
        assert user.username == user_info['username']
        assert user.password_hash is not None
        assert user.name == user_info['name']
        assert user.email == user_info['email']


def test_route_auth_sign_in(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    create_user(app, db)

    credentials = {
        'username': 'username123',
        'password': 'password123',
    }
    response = client.post('/api/auth/sign-in', json=credentials)
    assert response.status_code == 200
    assert list(response.get_json().keys()) == ['access_token', 'refresh_token']

    cookies = [ cookie.name for cookie in client.cookie_jar ]
    assert cookies == [ 'access_token_cookie', 'refresh_token_cookie' ]


def test_route_refresh_access_token_cookie(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    with app.app_context():
        user = User('username123', 'password123', 'name example', 'example@mail.com')
        db.session.add(user)
        db.session.commit()
        refresh_token = user.create_refresh_token()

    client.set_cookie('localhost/api/auth', 'refresh_token_cookie', refresh_token)
    response = client.post('/api/auth/refresh-access-token')
    assert response.status_code == 200
    assert list(response.get_json().keys()) == ['access_token']
    cookies = [ cookie.name for cookie in client.cookie_jar ]
    assert cookies == [ 'access_token_cookie', 'refresh_token_cookie' ]
    assert [ cookie.value for cookie in client.cookie_jar if cookie.name == 'refresh_token_cookie' ][0] == refresh_token


def test_route_auth_refresh_access_token_headers(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    with app.app_context():
        user = User('username123', 'password123', 'name example', 'example@mail.com')
        db.session.add(user)
        db.session.commit()
        refresh_token = user.create_refresh_token()

    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    response = client.post('/api/auth/refresh-access-token', headers=headers)
    assert response.status_code == 200
    assert list(response.get_json().keys()) == ['access_token']
    cookies = [ cookie.name for cookie in client.cookie_jar ]
    assert cookies == [ 'access_token_cookie' ]


def test_route_auth_sign_out_cookie(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    with app.app_context():
        user = User('username123', 'password123', 'name example', 'example@mail.com')
        db.session.add(user)
        db.session.commit()
        refresh_token = user.create_refresh_token()

    
    client.set_cookie('/api/auth', 'refresh_token_cookie', refresh_token)
    response = client.post('/api/auth/sign-out')
    assert response.status_code == 200
    assert response.get_json() == {"message": "logout successful"}
    assert len(client.cookie_jar) == 1
    assert list(client.cookie_jar)[0].name == 'refresh_token_cookie'
    assert list(client.cookie_jar)[0].expires == None


def test_route_auth_sign_out_headers(client: 'FlaskClient', app: 'Flask', db: 'SQLAlchemy'):
    with app.app_context():
        user = User('username123', 'password123', 'name example', 'example@mail.com')
        db.session.add(user)
        db.session.commit()
        refresh_token = user.create_refresh_token()

    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    response = client.post('/api/auth/sign-out', headers=headers)
    assert response.status_code == 200
    assert response.get_json() == {"message": "logout successful"}
    assert len(client.cookie_jar) == 0
