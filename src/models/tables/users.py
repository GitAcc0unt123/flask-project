from __future__ import annotations

# RFC 8018 published in 2017, recommends PBKDF2 for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from sqlalchemy.sql import func

from src.models.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False, default="")
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now()) # datetime.datetime.utcnow
    activated_at = db.Column(db.DateTime, nullable=True)


    def __init__(self, username: str, password: str, name: str, email: str):
        self.username = username
        self.password_hash = generate_password_hash(password, method='sha256')
        self.name = name
        self.email = email

    def create_access_token(self) -> str:
        access_token = create_access_token(identity=self.id)#, additional_claims=additional_claims)
        return access_token
    
    def create_refresh_token(self) -> str:
        refresh_token = create_refresh_token(identity=self.id)
        return refresh_token
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username: str, password: str) -> User | None:
        user = User.query.filter_by(username=username).one_or_none()
        if user == None or not user.check_password(password):
            return None
        return user
