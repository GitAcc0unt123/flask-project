import logging

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, InternalServerError
from marshmallow import ValidationError
from sqlalchemy import select, and_

from src.models import CompletedTest, db
from src.schemas import CompletedTestSchema


completed_test_bp = Blueprint('completed_test', __name__)


@completed_test_bp.route('', methods=['POST'])
@jwt_required(locations=['cookies', 'headers'])
def complete_test():
    input = request.json
    user_id = get_jwt_identity()
    try:
        validated_input = CompletedTestSchema(only=['test_id']).load(input)

        stmt = select(CompletedTest).where(and_(
                CompletedTest.test_id == validated_input['test_id'],
                CompletedTest.user_id == user_id)
        )
        completed_test = db.session.execute(stmt).scalar_one_or_none()

        if completed_test is None:
            completed_test = CompletedTest(**validated_input, user_id=user_id)
            db.session.add(completed_test)
            db.session.commit()
        return ('', 201)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()
