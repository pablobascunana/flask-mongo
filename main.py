import logging
import os

from dotenv import load_dotenv

load_dotenv()

from config import logger
from config.mongo import db
from config.marshmallow import marshmallow as ma
from config.swagger import SWAGGER_CONFIG
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flasgger import Swagger
from resources.routes.routes import create_resources
from utils.constants import JWT_ALGORITHM, JWT_IDENTITY_CLAIM
from utils.errors import create_error_handlers
from utils.jwt import create_token_callbacks

app = Flask(__name__)

logging.info('The server mode is: {}'.format(app.config['ENV']))
logging.info('The app is in debug mode: {}'.format(os.getenv('DEBUG')))

app.config['JWT_ALGORITHM'] = JWT_ALGORITHM
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=int(os.getenv('JWT_EXPIRATION_TIME')))
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_IDENTITY_CLAIM'] = JWT_IDENTITY_CLAIM
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.config["MONGODB_HOST"] = os.getenv('DATABASE')
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['SWAGGER'] = SWAGGER_CONFIG

swagger = Swagger(app)

api = Api(app)
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

create_error_handlers(app)
create_resources(api)
create_token_callbacks(jwt)

logging.info('The version number is: {}'.format(os.getenv('VERSION_NUMBER')))

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=os.getenv('DEBUG'))
