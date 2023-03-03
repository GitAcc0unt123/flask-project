from typing import TYPE_CHECKING

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.models import db
from src.routes import user_bp, test_bp, question_bp, question_answer_bp, completed_test_bp

if TYPE_CHECKING:
     from src.utils.config import Config


def create_flask_app(config: 'Config') -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(config)

    app.register_blueprint(user_bp, url_prefix='/api/auth')
    app.register_blueprint(test_bp, url_prefix='/api/tests')
    app.register_blueprint(completed_test_bp, url_prefix='/api/completed-test')
    app.register_blueprint(question_bp, url_prefix='/api')
    app.register_blueprint(question_answer_bp, url_prefix='/api/question-answer')

    JWTManager(app)
    CORS(app, 
         resources={r'/api/*': {'origins': ['http://localhost:80', 'https://localhost:443']}},
         supports_credentials=True
    )

    db.init_app(app)
    return app