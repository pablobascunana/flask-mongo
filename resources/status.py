import logging
import os

from flasgger import swag_from
from flask_restful import Resource
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from utils.constants import SWAGGER_PATH

DB_URI = os.getenv('DATABASE')
IS_ALIVE_ERROR = 'Audit server is not connected to mongodb database'
SWAGGER_STATUS_PATH = SWAGGER_PATH + 'status/'


class IsAlive(Resource):
    @classmethod
    @swag_from(SWAGGER_STATUS_PATH + 'is_alive.yml')
    def get(cls):
        if check_database_is_alive(DB_URI):
            logging.info('Audit server is alive')
            return 'Server is alive', 200

        logging.error(IS_ALIVE_ERROR)
        return 'Server is not alive', 500


class Version(Resource):
    @classmethod
    @swag_from(SWAGGER_STATUS_PATH + 'version.yml')
    def get(cls):
        return os.getenv('VERSION_NUMBER')


def check_database_is_alive(db_uri: str) -> bool:
    client = MongoClient(db_uri, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
    try:
        client.server_info()
        return True
    except ServerSelectionTimeoutError:
        return False
