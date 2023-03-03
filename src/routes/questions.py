import logging

from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, InternalServerError
from marshmallow import ValidationError
from sqlalchemy import select, and_

from src.models import Question, CompletedTest, Test, db
from src.schemas import QuestionSchema


question_bp = Blueprint('question', __name__)


@question_bp.route('tests/<int:test_id>/questions', methods=['POST'])
@jwt_required(locations=['cookies', 'headers'])
def create_question(test_id):
    input = request.json
    _ = db.get_or_404(Test, test_id)
    try:
        validated_input = QuestionSchema(exclude=['test_id']).load(input)
        question = Question(**validated_input, test_id=test_id)
        db.session.add(question)
        db.session.commit()
        return ({ 'id': question.id }, 201)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('tests/<int:test_id>/questions', methods=['GET'])
@jwt_required(locations=['cookies', 'headers'])
def get_test_questions(test_id):
    _ = db.get_or_404(Test, test_id)
    try:
        user_id = get_jwt_identity()
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()

    try:
        stmt = select(Question).where(Question.test_id == test_id).order_by(Question.id)
        questions = db.session.execute(stmt).scalars().all()
        stmt = select(1).where(and_(
            CompletedTest.test_id == test_id,
            CompletedTest.user_id == user_id
        ))
        completed_test = db.session.execute(stmt).scalar_one_or_none()

        if completed_test is None:
            result = QuestionSchema(exclude=['true_answers']).dump(questions, many=True)
        else:
            result = QuestionSchema().dump(questions, many=True)
        return result
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('tests/<int:test_id>/questions/<int:id>', methods=['GET'])
@jwt_required(locations=['cookies', 'headers'])
def get_question_by_id(test_id, id):
    _ = db.get_or_404(Test, test_id)
    question = db.get_or_404(Question, id)
    try:
        return QuestionSchema(exclude=['true_answers']).dump(question)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('tests/<int:test_id>/questions/<int:id>', methods=['PUT'])
@jwt_required(locations=['cookies', 'headers'])
def update_question(test_id, id):
    input = request.json
    _ = db.get_or_404(Test, test_id)
    question = db.get_or_404(Question, id)
    try:
        validated_input = QuestionSchema(exclude=['test_id']).load(input)
        question.update(validated_input | {'test_id': test_id})
        question.verified = True
        db.session.commit()
        return QuestionSchema().dump(question)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('tests/<int:test_id>/questions/<int:id>', methods=['DELETE'])
@jwt_required(locations=['cookies', 'headers'])
def delete_question(test_id, id):
    _ = db.get_or_404(Test, test_id)
    question = db.get_or_404(Question, id)
    try:
        db.session.delete(question)
        db.session.commit()
        return Response(status=204)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()
