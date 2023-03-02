import logging

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies, \
    set_refresh_cookies, unset_jwt_cookies
from werkzeug.exceptions import BadRequest, InternalServerError
from marshmallow import ValidationError
from sqlalchemy import select, insert

from src.models import User, db
from src.schemas import SignInSchema, SignUpSchema


user_bp = Blueprint('user', __name__)


@user_bp.route('/sign-in', methods=['POST'])
def sign_in():
    input = request.json
    try:
        validated_input = SignInSchema().load(input)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()

    user = User.authenticate(**validated_input)
    if user is None:
        raise BadRequest(description='Invalid username or password')

    ret = {
        'access_token': user.create_access_token(),
        'refresh_token': user.create_refresh_token()
    }
    response = jsonify(ret)
    set_access_cookies(response, ret['access_token'])
    set_refresh_cookies(response, ret['refresh_token'])
    return (response, 200)


@user_bp.route('/sign-up', methods=['POST'])
def sign_up():
    input_json = request.json
    try:
        validated_input = SignUpSchema().load(input_json)
        user = User(**validated_input)
        stmt = insert(User).values(
            username=user.username,
            password_hash=user.password_hash,
            name=user.name,
            email=user.email
        ).returning(User.id)
        with db.engine.connect() as conn:
            id = conn.execute(stmt).scalar_one_or_none()
            conn.commit()
            return ({ 'id': id }, 201)
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        logging.exception(type(err))
        raise InternalServerError()


@user_bp.route('/refresh-access-token', methods=['POST'])
@jwt_required(refresh=True, locations=['cookies', 'headers'])
def refresh_access_token():
    try:
        user_id = get_jwt_identity()
        user = db.session.execute(select(User).where(User.id == user_id)).scalar_one()
        ret = {
            'access_token': user.create_access_token(),
        }
        response = jsonify(ret)
        set_access_cookies(response, ret['access_token'])
        return (response, 200)
    except Exception as err:
        logging.exception(str(err))
        raise InternalServerError()


@user_bp.route("/sign-out", methods=["POST"])
@jwt_required(refresh=True, locations=['cookies', 'headers'])
def sign_out():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response
