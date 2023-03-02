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
