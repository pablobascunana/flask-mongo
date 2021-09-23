import os
import pytest

from dotenv import load_dotenv

load_dotenv()

from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from models.user import User as UserModel
from mongoengine import connect, disconnect
from schemas.user import UserSchema
from usecases.user import do_user_login
from utils.commons import generate_hash_password
from utils.constants import JWT_ALGORITHM, JWT_IDENTITY_CLAIM


MOCKED_DB_NAME = 'test'
user_schema = UserSchema()


@pytest.fixture
def load_user():
    connect(MOCKED_DB_NAME, host='mongomock://localhost:27017')
    return user_schema.load({
        "userName": "test",
        "name": "Pepe",
        "lastName": "Perez Lopez",
        "email": "uncorreo@email.com",
        "password": "1234"
    }, partial=True)


@pytest.fixture
def app_and_login_user():
    app = create_flask_app()
    connect(MOCKED_DB_NAME, host='mongomock://localhost:27017')
    return app, user_schema.load({"userName": "test", "password": "1234"}, partial=True)


def create_flask_app():
    app = Flask(__name__)
    app.config['JWT_ALGORITHM'] = JWT_ALGORITHM
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=30)
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_IDENTITY_CLAIM'] = JWT_IDENTITY_CLAIM
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    JWTManager(app)
    return app


def test_insert_user(load_user):
    load_user.password = generate_hash_password(load_user.password)
    user = UserModel.insert(load_user)
    assert user.id is not None
    assert user.userName == load_user.userName
    assert user.name == load_user.name
    assert user.lastName == load_user.lastName
    assert user.email == load_user.email
    assert user.password == load_user.password
    assert user.loginAttempts == 0
    assert user.registerDate is not None
    dumped_user = user_schema.dump(user)
    assert len(dumped_user) == 4
    assert dumped_user['userName'] == load_user.userName
    assert dumped_user['name'] == load_user.name
    assert dumped_user['lastName'] == load_user.lastName
    assert dumped_user['email'] == load_user.email
    disconnect(MOCKED_DB_NAME)


def test_do_success_login(app_and_login_user):
    db_user = UserModel.get_user_by_username(app_and_login_user[1])
    with app_and_login_user[0].app_context():
        response = do_user_login(app_and_login_user[1], db_user)
        assert 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9' in response[0].get("access_token")
        assert 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9' in response[0].get("refresh_token")
        assert response[1] == 200


def test_do_incorrect_login(app_and_login_user):
    app_and_login_user[1].password = "12344"
    db_user = UserModel.get_user_by_username(app_and_login_user[1])
    response = do_user_login(app_and_login_user[1], db_user)
    assert response[0].get("message") == 'Bad credentials'
    assert response[1] == 401
