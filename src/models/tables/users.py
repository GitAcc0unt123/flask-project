from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.sql import select, func

from src.models.database import db

if TYPE_CHECKING:
    from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(255), nullable=False, unique=True)
    password_hash: str = db.Column(db.String(255), nullable=False)
    name: str = db.Column(db.String(255), nullable=False, default="")
    email: str = db.Column(db.String(255), nullable=False, unique=True)
    created_at: Optional[datetime] = db.Column(db.DateTime, nullable=False, default=func.now())
    activated_at: Optional[datetime] = db.Column(db.DateTime, nullable=True)


    def __init__(self, username: str, password: str, name: str, email: str):
        self.username = username
        self.password_hash = generate_password_hash(password, method='sha256')
        self.name = name
        self.email = email

    def create_access_token(self) -> str:
        access_token = create_access_token(identity=self.id)
        return access_token
    
    def create_refresh_token(self) -> str:
        refresh_token = create_refresh_token(identity=self.id)
        return refresh_token
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional[User]: # Optional[Self] in python 3.11
        user = db.session.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if user is None or not user.check_password(password):
            return None
        return user
