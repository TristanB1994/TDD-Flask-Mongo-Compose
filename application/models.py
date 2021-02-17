import os
from flask_mongoengine import MongoEngine
from flask_user import UserMixin

db = MongoEngine()

class User(db.Document, UserMixin):

    meta = {'db_alias':'registry'}

    active = db.BooleanField(default=False)

    # User authentication information
    email = db.StringField(default='')
    username = db.StringField(default='')
    password = db.StringField()
    email_confirmed_at = db.DateTimeField(default=None)

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')

    # Relationships
    roles = db.StringField(default='end-user')

    def __repr__(self):
        return f"<User {self.username}>"
    
    def __str__(self):
        return f"<User: {self.username}"