from flask import Flask
from application.models import User
from application.extensions import admin, user_manager, serializer
import os

try:
    from application.models import db, User
except Exception as error:
    print(f"Failed to import db class: {error}")

import json


def create_app(config_name):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    # Reset mongodb from env str to dict for flask_mongoengine init
    app.config['MONGODB_SETTINGS'] = json.loads(app.config['MONGODB_SETTINGS'])
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    for k,v in app.config.items():
        print(f"app_var {k}: {v}")
        
    register_extensions(app)

    # eventuall register blueprints here
    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/users")
    def users():
        try:
            num_users = User.query.count()
            return f"Number of users: {num_users}"
        except:
            return f"No users"

    return app

def register_extensions(app):

    db.init_app(app)
    # app.db = db.get_db(app.config['MONGODB_SETTINGS']['db'])
    # print(f"app.db: {app.db}")

    serializer(app.secret_key)

    user_manager(app, db, User)

    admin.init_app(app)

    # from app.admin_core import configure_admin
    # configure_admin(admin)
    
    return None
