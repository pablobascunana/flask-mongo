import logging
import os

from dotenv import load_dotenv

load_dotenv()

from config import logger
from flask import Flask
from flask_restful import Api


app = Flask(__name__)

logging.info('The server mode is: {}'.format(app.config['ENV']))
logging.info('The app is in debug mode: {}'.format(os.getenv('DEBUG')))

api = Api(app)

logging.info('The version number is: {}'.format(os.getenv('VERSION_NUMBER')))

if __name__ == "__main__":
    app.run(port=5000, debug=os.getenv('DEBUG'))
