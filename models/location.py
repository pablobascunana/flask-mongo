from bson.objectid import ObjectId
from config.mongo import db
from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField


class Marker(EmbeddedDocument):
    position = db.DictField(required=True)
    title = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow, required=True)


class Location(db.Document):
    userId = db.ObjectIdField(required=True)
    markers = db.ListField(EmbeddedDocumentField(Marker), required=True)

    @classmethod
    def insert_or_update(cls, location: "Location") -> "Location":
        return cls.objects(userId=location.userId).modify(upsert=True, new=True, markers=location.markers)

    @classmethod
    def get_locations_by_user_id(cls, userId: str) -> "Location":
        return cls.objects.get(userId=ObjectId(userId))

    @classmethod
    def delete_marker(cls, userId: str, marker: "Marker") -> "Location":
        '''https://stackoverflow.com/questions/10269056/using-mongodb-how-do-you-remove-embedded-document-from-a-list-based-on-a-match'''
        return cls.objects(userId=userId).update_one(
            pull__markers__title=Marker(title=marker.title).title)
