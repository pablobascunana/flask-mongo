import logging
import configparser

from marshmallow import ValidationError
from mongoengine import DoesNotExist, ValidationError as ValidationErr, NotUniqueError
from pymongo.errors import DuplicateKeyError
from utils.responses import bad_request, not_found


def create_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation_error(error):
        logging.error(error.messages)
        return bad_request(error.messages)

    @app.errorhandler(ValidationErr)
    def handle_mongoengine_validation_error(error):
        logging.error(error.message)
        return bad_request(error.message)

    @app.errorhandler(DoesNotExist)
    def handle_does_not_exist_error(error):
        logging.error(error.args[0])
        return not_found(error.args[0])

    @app.errorhandler(NotUniqueError)
    def handle_does_not_exist_error(error):
        logging.error(error.args[0])
        return bad_request(error.args[0])

    @app.errorhandler(DuplicateKeyError)
    def handle_duplicate_key_error(error):
        logging.error(error.args[0])
        return bad_request(error.args[0])

    @app.errorhandler(KeyError)
    def handle_key_error(error):
        logging.error(error.messages)
        return not_found(error.messages)

    @app.errorhandler(configparser.NoSectionError)
    def handle_no_section_error(error):
        logging.error(error.messages)
        return not_found(error.messages)

    @app.errorhandler(configparser.NoOptionError)
    def handle_no_option_error(error):
        logging.error(error.messages)
        return not_found(error.messages)

    @app.errorhandler(AttributeError)
    def handle_attribute_error(error):
        logging.error(error.args[0])
        return bad_request(error.args[0])
