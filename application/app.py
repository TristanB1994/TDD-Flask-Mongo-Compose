from flask import Flask, url_for

from application.front_blueprint import front_blueprint
from application.extensions import admin, serializer, debug_toolbar, security
# user_manager
from flask_security import hash_password #, auth_required, MongoEngineUserDatastore

from flask_admin import helpers as admin_helpers

from application.models import db, user_datastore, User, Role

import json
import os

def create_app(config_name):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    # Reset mongodb from env str to dict for flask_mongoengine init
    app.config['MONGODB_SETTINGS'] = json.loads(app.config['MONGODB_SETTINGS'])
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    # Flask-Security configs push to json file
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    

    # Flask-Security test configs
    app.config['LOGIN_DISABLED'] = True

    if config_name == 'development':
        app.config['DEBUG_TB_PANELS'] = json.loads(app.config['DEBUG_TB_PANELS'])

    # for k,v in app.config.items():
    #     print(f"app_var {k}: {v}")
        
    register_extensions(app, user_datastore)

    # Register Blueprints
    register_blueprints(app)

    @app.before_first_request
    def create_user():
        print("=========="*3)
        print(f"prerun function")
        if not user_datastore.find_user(email="test@me.com"):
            user_datastore.create_user(email="test@me.com", password=hash_password("password"))
            
        user = user_datastore.find_user(email="test@me.com")
        print(user)
        print("=========="*3)
    #     first_user = user_manager.create_user(email='admin', password='password')
    #     user_datastore.toggle_active(first_user)
    #     db.session.commit()
   
    # @user_manager.login_manager.context_processor
    # def security_context_processor():
    #     return dict(
    #         admin_base_template = admin.base_template,
    #         admin_view = admin.index_view,
    #         h = admin_helpers,
    #         get_url = url_for
    #     )


    return app

# def register_extensions(app, user_datastore):
def register_extensions(app, user_datastore):

    db.init_app(app)
    app.db = db

    serializer(app.secret_key)

    # user_manager(app, app.db, User)
    # print(f"user manager: {dir(user_manager)}")

    admin.init_app(app)

    debug_toolbar(app)

    # security(app, user_datastore)
    security.init_app(app, user_datastore)

    # define a context processor for merging flask-admin's template context into the
    # flask-security views.
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # Access front bluprint and add context variables for Flask-admin layout 
    @front_blueprint.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # from app.admin_core import configure_admin
    # configure_admin(admin)
    
    return None

def register_blueprints(app):
    app.register_blueprint(front_blueprint)
    return None
