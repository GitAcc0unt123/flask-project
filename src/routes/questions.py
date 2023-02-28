import logging

from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, InternalServerError
from marshmallow import ValidationError
from sqlalchemy import select, and_

from src.models import Question, CompletedTest, db
from src.schemas import QuestionSchema


question_bp = Blueprint('question', __name__)


@question_bp.route('', methods=['POST'])
@jwt_required(locations=['cookies', 'headers'])
def create_question():
    input = request.json
    try:
        validated_input = QuestionSchema(exclude=['id']).load(input)
        question = Question(**validated_input)
        db.session.add(question)
        db.session.commit()
        return ({ 'id': question.id }, 201)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('', methods=['GET'])
@jwt_required(locations=['cookies', 'headers'])
def get_test_questions():
    test_id = request.args.get('test_id')
    if test_id is None:
        raise BadRequest('set test_id param in query string')
    
    user_id = get_jwt_identity()
    try:
        test_id = int(test_id)
        stmt = select(Question).where(Question.test_id==test_id).order_by(Question.id)
        questions = db.session.execute(stmt).scalars().all()
    except Exception as err:
        logging.exception(err)
        raise BadRequest('invalid test_id param in query string')
    
    stmt = select(1).where(and_(
        CompletedTest.test_id==test_id,
        CompletedTest.user_id==user_id
    ))
    completed_test = db.session.execute(stmt).scalar_one_or_none()

    try:
        if completed_test is None:
            result = QuestionSchema(exclude=['true_answers']).dump(questions, many=True)
        else:
            result = QuestionSchema().dump(questions, many=True)
        return result
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('/<int:id>', methods=['GET'])
@jwt_required(locations=['cookies', 'headers'])
def get_question_by_id(id):
    question = db.get_or_404(Question, id)
    try:
        return QuestionSchema(exclude=['true_answers']).dump(question)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('/<int:id>', methods=['PUT'])
@jwt_required(locations=['cookies', 'headers'])
def update_question(id):
    input = request.json
    question = db.get_or_404(Question, id)
    try:
        validated_input = QuestionSchema(exclude=['id', 'test_id'], partial=True).load(input)
        if validated_input is None or len(validated_input) == 0:
            raise BadRequest("empty input. fill at least one field")

        question.update(validated_input)
        question.verified = True
        db.session.commit()
        return QuestionSchema(only=validated_input.keys()).dump(question)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()


@question_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required(locations=['cookies', 'headers'])
def delete_question(id):
    question = db.get_or_404(Question, id)
    try:
        db.session.delete(question)
        db.session.commit()
        return Response(status=204)
    except Exception as err:
        logging.exception(err)
        raise InternalServerError()
