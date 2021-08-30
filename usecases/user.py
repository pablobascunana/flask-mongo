from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User as UserModel
from utils.commons import check_hash_password
from utils.responses import ok, unauthorized


def do_user_login(user: UserModel, stored_user: UserModel) -> tuple:
    if check_hash_password(user.password, stored_user.password) and stored_user.loginAttempts < 5:
        access_token = create_access_token(identity=create_payload(stored_user), fresh=True)
        refresh_token = create_refresh_token(user.id)
        return ok({"access_token": access_token, "refresh_token": refresh_token})
    else:
        return unauthorized({"message": "Bad credentials"})


def create_payload(user: UserModel) -> dict:
    return {
        "userUuid": str(user.id)
    }
