import pytest
import json
from flask import Flask, request, url_for
from flask.testing import FlaskClient

from application.app import create_app

# from mongoengine.context_managers import switch_db
# from flask_mongoengine import MongoEngine

from mongoengine import disconnect


@pytest.fixture(scope='function')
def flask_app():

    app = create_app("testing")
    # app.db.disconnect
    with app.app_context():
        # print("=========="*2)
        # for x in dir(app.login_manager):
        #     print(f"login manager: {x}")
        # print("=========="*2)
        # for x in dir(app.user_manager):
        #     print(f"user manager: {x}")
        # print("=========="*2)
        yield app


@pytest.fixture(scope='function')
def client(flask_app):
    with flask_app.test_request_context():

        with flask_app.test_client() as client:

            yield client

            # Potentially teardown client


@pytest.fixture(scope="function")
def login(client):
    url = url_for('security.login')
    yield client.post(url, data={'email':'test@me.com', 'password':'password'}, follow_redirects=True)


@pytest.fixture(scope="function")
def database(flask_app):
    # with app.app_context():        
        # db = app.db.get_db('testing')

    db = flask_app.db.get_db('testing')
        
    yield db

    # with app.app_context():

    #     colls = db.list_collection_names()
    #     for i in colls:
    #         db.drop_collection(i)
    #     print(f"list collections: {db.list_collection_names()}")

    print(f"Users: {[x for x in db.user.find()]}")
    colls = db.list_collection_names()
    for i in colls:
        db.drop_collection(i)
    print(f"list collections: {db.list_collection_names()}")
    
    db = flask_app.db.disconnect()

@pytest.fixture(scope="function")
def load_admin_data():
    with open("tests/user_data.json") as f:
        userJSON = json.load(f)[0]
        f.close()

    userDICT = {} 

    for key, value in userJSON['value'].items():
        try:
            userDICT[key] = value 
        except Exception as error:
            print(f"userDICT variable: {key}:{value} : {error}")

    return userDICT
    

# @pytest.fixture(scope='function')
# def register

@pytest.fixture(scope="function")
def bp_routes():
    def get_bp_routes(bp, method="GET"):  
        temp_app = Flask('test_app')
        temp_app.register_blueprint(bp)
        # Captures url routes for blueprint
        # if method:

        rules = [ r for r in temp_app.url_map.iter_rules() if (str(method) in r.methods and not "static" in r.rule ) ]
        # print(f"rules {rules}")
        
        return rules
    return get_bp_routes

@pytest.fixture(scope="function")
def flask_user_routes(flask_app):
    def get_flask_user_routes(method="GET"):  
        # Captures url routes for flask_user

        flask_user_rules = [ x for x in flask_app.url_map.iter_rules() if ( 'user' in x.rule.split('/') and not "static" in x.rule and str(method) in x.methods ) ]
        
        # print(f"rules {flask_user_rules}")
        
        return flask_user_rules
    return get_flask_user_routes