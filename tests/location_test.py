import bson
import pytest

from mongoengine import connect, disconnect
from models.location import Location as LocationModel
from schemas.location import LocationSchema, MarkerSchema


MOCKED_DB_NAME = 'test'
location_schema = LocationSchema()
marker_schema = MarkerSchema()


@pytest.fixture
def location():
    connect(MOCKED_DB_NAME, host='mongomock://localhost:27017')
    return location_schema.load({
      "markers": [
        {
          "position": {
            "lat": 40.1054808,
            "lng": -2.221822
          },
          "title": "Cuenca"
        }
      ],
      "userId": "61313181b85829288a1bb9f4"
    }, partial=True)


def test_save_location(location):
    location = LocationModel.insert_or_update(location)
    assert bson.objectid.ObjectId.is_valid(location.userId)
    assert len(location.markers) == 1
    assert type(location.markers[0].position.get('lat')) is float
    assert type(location.markers[0].position.get('lng')) is float
    assert type(location.markers[0].title) is str
    assert str(location.userId) == "61313181b85829288a1bb9f4"
    assert location.markers[0].position.get('lat') == 40.1054808
    assert location.markers[0].position.get('lng') == -2.221822
    assert location.markers[0].title == "Cuenca"


def test_get_location(location):
    locations = LocationModel.get_locations_by_user_id(location.userId)
    assert len(locations.markers) == 1


def test_delete_location(location):
    LocationModel.delete_marker(userId=location.userId, marker=location.markers[0])
    locations = LocationModel.get_locations_by_user_id(location.userId)
    assert len(locations.markers) == 0
    disconnect(MOCKED_DB_NAME)
