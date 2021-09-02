from flasgger import swag_from
from flask import request
from flask_restful import Resource
from schemas.user import UserSchema
from models.user import User as UserModel
from usecases.user import do_user_login
from utils.commons import generate_hash_password
from utils.constants import SWAGGER_PATH
from utils.responses import created

user_schema = UserSchema()
SWAGGER_STATUS_PATH = SWAGGER_PATH + 'user/'


class User(Resource):
    @classmethod
    @swag_from(SWAGGER_STATUS_PATH + 'user.yml')
    def post(cls):
        user = user_schema.load(request.get_json(), partial=True)
        user.password = generate_hash_password(user.password)
        user = UserModel.insert(user)
        return created(user_schema.dump(user))


class Login(Resource):
    @classmethod
    @swag_from(SWAGGER_STATUS_PATH + 'login.yml')
    def post(cls):
        user = user_schema.load(request.get_json(), partial=True)
        db_user = UserModel.get_user_by_username(user)
        return do_user_login(user, db_user)
