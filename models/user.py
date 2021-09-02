from config.mongo import db
from datetime import datetime


class User(db.Document):
    userName = db.StringField(required=True)
    name = db.StringField(required=True)
    lastName = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    loginAttempts = db.IntField(default=0)
    registerDate = db.DateField(default=datetime.now())
    lastLoginDate = db.DateField()

    meta = {
        'indexes': [
            {'fields': ('userName',), 'unique': True},
            {'fields': ('email',), 'unique': True}
        ]
    }

    @classmethod
    def insert(cls, user: "User") -> "User":
        return user.save()

    @classmethod
    def get_user_by_username(cls, user: "User") -> "User":
        return cls.objects.get(userName=user.userName)
