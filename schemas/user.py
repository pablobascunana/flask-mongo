from marshmallow_mongoengine import ModelSchema
from models.user import User as UserModel


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel
        model_fields_kwargs = {
            'id': {'load_only': True},
            'password': {'load_only': True},
            'verified': {'load_only': True},
            'state': {'load_only': True},
            'role': {'load_only': True},
            'loginAttempts': {'load_only': True},
            'registerDate': {'load_only': True},
            'lastLoginDate': {'load_only': True}
        }
