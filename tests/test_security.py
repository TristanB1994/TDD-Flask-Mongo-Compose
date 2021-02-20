from flask import request, g, session, url_for
from flask_security.datastore import MongoEngineDatastore
from flask_security import current_user

def test__login_get(client):
    print(f"\n")

    url = url_for('security.login')
    response = client.get(url, follow_redirects=True)

    assert response.status_code == 200

def test__login_post_pass(client, login): # flask_app
    print(f"\n")

    print(f"request: {request}")
    print(f"session: {session}")
    print(f"current user id: {current_user.get_id()}")

    url = url_for('admin.index')
    response = client.get(url, follow_redirects=True)
    # response = login

    print(f"request: {request}")
    print(f"session: {session}")
    print(f"current user id: {current_user.get_id()}")

    assert response.status_code == 200


def test__check_security_in_app_extensions(flask_app):

    with flask_app.test_request_context():

        with flask_app.test_client() as client:

            # print(f"datastore: {flask_app.extensions['security'].datastore}")            
            datastore = flask_app.extensions['security'].datastore

            assert isinstance(datastore, MongoEngineDatastore)
            

