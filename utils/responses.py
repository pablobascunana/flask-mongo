from flask_api import status


def created(json_data: dict):
    return json_data, status.HTTP_201_CREATED
