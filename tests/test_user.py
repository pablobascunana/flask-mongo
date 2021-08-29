import pytest

from mongoengine import connect, disconnect

from models.user import User as UserModel
from schemas.user import UserSchema
from utils.commons import generate_hash_password


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


def test_insert_user(load_user):
    load_user.password = generate_hash_password(load_user.password)
    user = UserModel.insert(load_user)
    assert user.id is not None
    assert user.userName == load_user.userName
    assert user.name == load_user.name
    assert user.lastName == load_user.lastName
    assert user.email == load_user.email
    assert user.password == load_user.password
    assert user.verified is False
    assert user.state == load_user.state
    assert user.role == load_user.role
    assert user.loginAttempts == 0
    assert user.registerDate is not None
    dumped_user = user_schema.dump(user)
    assert len(dumped_user) == 4
    assert dumped_user['userName'] == load_user.userName
    assert dumped_user['name'] == load_user.name
    assert dumped_user['lastName'] == load_user.lastName
    assert dumped_user['email'] == load_user.email
    disconnect(MOCKED_DB_NAME)
