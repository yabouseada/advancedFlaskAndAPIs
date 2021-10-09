from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jti,
    get_jwt,
)
from flask_restful import Resource
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from marshmallow import ValidationError


USER_ALREADY_EXISTS = "A USER WITH THAT USERNAME ALREADY EXISTS"
CREATED_SUCCESSFULLY = "USE CREATED SUCCESSFULLY"
USER_NOT_FOUND = "USER NOT FOUND"
USER_DELETED = "USER DELETED"
INVALID_CREDENTIALS = "INVALID CREDENTIAS"
USER_LOGGED_OUT = "USER <id={user_id}> LOGGED OUT"
NOT_CONFIRMED_ERROR = (
    "you have not confirmed your registration, please check your email <{}>."
)
USER_CONFIRMED = "YOUR USER HAS BEEN CONFIRMED"
user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class UserReview(Resource):
    @classmethod
    def get(cls):

        return {"username": [user.json() for user in UserModel.query.all()]}


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user_schema.dump(user)

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            return {"message": NOT_CONFIRMED_ERROR.format(user.username)}, 400
        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        user_id = get_jwt_identity()
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id=user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserConfirmed(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}

        user.activated = True
        user.save_to_db()
        return {"message": USER_CONFIRMED}, 200
