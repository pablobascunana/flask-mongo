from flask import jsonify
from flask_api import status


def ok(json_data: dict) -> tuple:
    return json_data, status.HTTP_200_OK


def created(json_data: dict) -> tuple:
    return json_data, status.HTTP_201_CREATED


def bad_request(message: dict) -> tuple:
    return jsonify(message), status.HTTP_400_BAD_REQUEST


def unauthorized(message: dict) -> tuple:
    return message, status.HTTP_401_UNAUTHORIZED


def forbidden(message: dict) -> tuple:
    return jsonify(message), status.HTTP_403_FORBIDDEN


def not_found(message: dict) -> tuple:
    return jsonify(message), status.HTTP_404_NOT_FOUND


def conflict(message: dict) -> tuple:
    return jsonify(message), status.HTTP_409_CONFLICT


def internal_server_error(message: dict):
    return jsonify(message), status.HTTP_500_INTERNAL_SERVER_ERROR
