import pytest
import json

from application.app import create_app

from mongoengine.context_managers import switch_db
from flask_mongoengine import MongoEngine
from mongoengine import connect, disconnect


@pytest.fixture
def app():

    app = create_app("testing")
    # app.db.disconnect
    return app


@pytest.fixture(scope="function")
def database(app):
    with app.app_context():
        
        db = app.db.get_db('testing')
        # db = MongoEngine(app) #.get_db('testing')
        # db = connect('testing', host='0.0.0.0', username='admin', password='password', alias='testing')

        print(f"db {db}")
        
    yield db

    with app.app_context():

        colls = db.list_collection_names()
        for i in colls:
            db.drop_collection(i)
        print(f"list collections: {db.list_collection_names()}")

    db = app.db.disconnect()

@pytest.fixture(scope="function")
def load_user_data():
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