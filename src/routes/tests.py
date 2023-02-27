import logging

from flask import Blueprint, Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, InternalServerError
from marshmallow import ValidationError
from sqlalchemy import select, insert, update

from src.models import Test, db
from src.schemas import TestSchema

# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage

test_bp = Blueprint('test', __name__)


@test_bp.route('', methods=['GET'])
def get_all_tests():
    try:
        tests = db.session.execute(select(Test).order_by(Test.id)).scalars().all()
        result = TestSchema(only=['id', 'title', 'description']).dump(tests, many=True)
        logging.error(tests)
        return result
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()


@test_bp.route('', methods=['POST'])
@jwt_required(locations=['cookies', 'headers'])
def create_test():
    input = request.json
    try:
        validated_input = TestSchema(exclude=['id']).load(input)
        # test = Test(**validated_input)
        # db.session.add(test)
        # db.session.commit()
        with db.engine.connect() as conn:
            stmt = insert(Test).values(**validated_input).returning(Test.id)
            id = conn.execute(stmt).scalar_one_or_none()
            conn.commit()
            return ({ 'id': id }, 201)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()


@test_bp.route('/<int:id>', methods=['GET'])
@jwt_required(locations=['cookies', 'headers'])
def get_test_by_id(id):
    test = db.get_or_404(Test, id)
    try:
        return TestSchema().dump(test)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()


@test_bp.route('/<int:id>', methods=['PUT'])
@jwt_required(locations=['cookies', 'headers'])
def update_test(id):
    input = request.json
    try:
        validated_input = TestSchema(exclude=['id'], partial=True).load(input)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()

    if validated_input == None or len(validated_input) == 0:
        raise BadRequest("empty input. fill at least one field")

    test = db.get_or_404(Test, id)
    try:
        test.update(validated_input)
        test.verified = True
        db.session.commit()
        response = TestSchema(only=validated_input.keys()).dump(test)
        return response
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()


@test_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required(locations=['cookies', 'headers'])
def delete_test(id):
    test = db.get_or_404(Test, id)
    try:
        db.session.delete(test)
        db.session.commit()
        return Response(status=204)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()
