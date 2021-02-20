import os
from flask_mongoengine import MongoEngine
# from flask_user import UserMixin

from flask_security import UserMixin, RoleMixin, MongoEngineUserDatastore

db = MongoEngine()

ALIAS = os.getenv('MONGO_INITDB_DATABASE')
print(f"alias: {ALIAS}")

# class User(db.Document): #, UserMixin):

#     meta = {'db_alias':ALIAS}

#     active = db.BooleanField(default=False)

#     # User authentication information
#     email = db.StringField(default='')
#     username = db.StringField(default='')
#     password = db.StringField()
#     email_confirmed_at = db.DateTimeField(default=None)

#     # User information
#     first_name = db.StringField(default='')
#     last_name = db.StringField(default='')

#     # Relationships
#     roles = db.StringField(default='end-user')

#     def __repr__(self):
#         return f"<User {self.username}>"
    
#     def __str__(self):
#         return f"<User: {self.username}"

#     def _get_email(self):
#         return self.email


class Role(db.Document, RoleMixin):

    meta = {'db_alias':ALIAS}

    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    permissions = db.StringField(max_length=255)

class User(db.Document, UserMixin):

    meta = {'db_alias':ALIAS}

    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    fs_uniquifier = db.StringField(max_length=64, unique=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def _get_email(self):
        return self.email

    def __repr__(self):
        return f"<User {self.email}>"
    
    def __str__(self):
        return f"<User {self.email}>"

user_datastore = MongoEngineUserDatastore(db, User, Role)
