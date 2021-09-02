from marshmallow_mongoengine import ModelSchema
from models.location import Location as LocationModel, Marker as MarkerModel


class MarkerSchema(ModelSchema):
    class Meta:
        model = MarkerModel


class LocationSchema(ModelSchema):
    class Meta:
        model = LocationModel

        model_fields_kwargs = {
            'id': {'load_only': True}
        }
