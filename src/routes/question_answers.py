import logging

from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, InternalServerError
from marshmallow import ValidationError
from sqlalchemy import select, and_, exists

from src.models import QuestionAnswer, Question, Test, db
from src.schemas import QuestionAnswerSchema


question_answer_bp = Blueprint('question_answer', __name__)


@question_answer_bp.route('', methods=['GET'])
@jwt_required(locations=['cookies', 'headers'])
def get_question_answers():
    user_id = get_jwt_identity()
    test_id = request.args.get('test_id')
    if test_id is None:
        raise BadRequest('set test_id param in query string')

    try:
        test_id = int(test_id)
        exists_criteria = select(1).where(Test.id == test_id).exists()
        stmt = select(1).where(exists_criteria)
        test_id_exist = db.session.execute(stmt).scalar_one_or_none()
    except ValueError as err:
        raise BadRequest('incorrect test_id')
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()
    
    if test_id_exist is None:
        raise BadRequest('incorrect test_id')
    
    try:
        stmt = select(QuestionAnswer).where(
                and_(
                    QuestionAnswer.user_id == user_id,
                    QuestionAnswer.question_id.in_(
                        select(Question.id).where(Question.test_id==test_id)
                    )
            ))
        question_answers = db.session.execute(stmt).scalars().all()
        result = QuestionAnswerSchema().dump(question_answers, many=True)
        return result
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()


@question_answer_bp.route('', methods=['POST'])
@jwt_required(locations=['cookies', 'headers'])
def create_or_update_question_answer():
    input = request.json
    user_id = get_jwt_identity()

    try:
        validated_input = QuestionAnswerSchema(only=['question_id', 'answer']).load(input)
        question_answer = QuestionAnswer.query\
            .filter(and_(
                    QuestionAnswer.question_id==validated_input['question_id'],
                    QuestionAnswer.user_id==user_id))\
            .one_or_none()

        if question_answer is None:
            question_answer = QuestionAnswer(**validated_input, user_id=user_id)
            db.session.add(question_answer)
        else:
            question_answer.update(validated_input)
            question_answer.verified = True
        db.session.commit()
        return Response(status=201)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()