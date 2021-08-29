import datetime

from config.mongo import db


class User(db.Document):
    userName = db.StringField(required=True)
    name = db.StringField(required=True)
    lastName = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    verified = db.BooleanField(default=False)
    state = db.StringField(default='INACTIVE')
    role = db.StringField(default='ADMIN')
    loginAttempts = db.IntField(default=0)
    registerDate = db.DateField(default=datetime.datetime.now())
    lastLoginDate = db.DateField()

    meta = {
        'indexes': [
            {'fields': ('userName',), 'unique': True},
            {'fields': ('email',), 'unique': True}
        ]
    }