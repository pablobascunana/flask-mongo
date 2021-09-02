from flasgger import swag_from
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from schemas.location import LocationSchema, MarkerSchema
from models.location import Location as LocationModel
from utils.constants import SWAGGER_PATH
from utils.responses import created, ok

location_schema = LocationSchema()
marker_schema = MarkerSchema()
SWAGGER_STATUS_PATH = SWAGGER_PATH + 'location/'

# TODO securizar con el jwt


class Location(Resource):
    @classmethod
    @jwt_required()
    @swag_from(SWAGGER_STATUS_PATH + 'location.yml')
    def get(cls, user_uuid):
        markers = LocationModel.get_locations_by_user_id(user_uuid)
        return created(location_schema.dump(markers))

    @classmethod
    @jwt_required()
    @swag_from(SWAGGER_STATUS_PATH + 'location.yml')
    def post(cls, user_uuid):
        location = location_schema.load(request.get_json(), partial=True)
        location = LocationModel.insert_or_update(location)
        return created(location_schema.dump(location))

    @classmethod
    @jwt_required()
    @swag_from(SWAGGER_STATUS_PATH + 'location.yml')
    def delete(cls, user_uuid):
        marker = marker_schema.load(request.get_json(), partial=True)
        LocationModel.delete_marker(userId=user_uuid, marker=marker)
        return ok(location_schema.dump(LocationModel.get_locations_by_user_id(user_uuid)))
