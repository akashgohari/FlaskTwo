import hmac

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
                                get_jwt)
from flask_restful import Resource

from blacklist import BLACKLIST
from models.user import UserModel
from schemas.user import UserSchema

_user_schema = UserSchema()


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user = _user_schema.load(request.get_json())
        user_exist = UserModel.find_by_username(user.username)
        if user_exist and hmac.compare_digest(user_exist.password, user.password):
            return {
                "access_token": create_access_token(identity=user.id, fresh=True),
                "refresh_token": create_refresh_token(user.id),
            }
        return {"message": "Invalid Credential"}, 401


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = _user_schema.load(request.get_json())
        if UserModel.find_by_username(user.username):
            return {"message": "User already exists"}, 400
        user.add_update_user()
        return {"message": "Successfully added user"}, 201


class User(Resource):
    @classmethod
    def get(cls, name):
        user = UserModel.find_by_username(name)
        if user:
            return {'user': _user_schema.dump(user)}
        return {"message": "User does not exists"}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        return {"access_token": create_access_token(identity=current_user, fresh=False)}


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        access_id = get_jwt()['jti']
        BLACKLIST.add(access_id)
