from application.models import User
from lxml import html
from flask import request, g, session, url_for
from flask_security import hash_password

def test__register_get(client):
    response = client.get('/register')
    # print(f"response: {response}, status: {response.status_code}, data: {response.data}")
    
    # tree = html.fromstring(response.data)
    # print(f"tree: {dir(tree)}")

    # print(f"tree str: {html.tostring(tree)}")
    # print(f"form str: {html.tostring(tree.forms[0])}")
    
    # form_inputs = tree.forms[0].xpath('//input')
    # print(f"form_inputs: {form_inputs}")
    
    assert response.status_code == 200

"""
def test__register_post(client, load_admin_data):
    user = load_admin_data
    print(f"register_post user: {user}")
    user_data = {
        "username":user['username'],
        "password":user['password']
        }
    register_response = client.post('/user/register', data=user_data, follow_redirects=True)

    client.preserve_context = True

    login_response = client.post('/user/sign-in', data=user_data, follow_redirects=True)
    # print(f"request: {request}")

    client.preserve_context = True

    with client.preserve_context():

        admin_response = client.get('/admin/')
        print(f"response: {admin_response}, status: {admin_response.status_code}")
        assert admin_response.status_code == 200
    # print(f"headers: {response.headers}")
    # print(f"location: {response.location}")
    # print(f"status: {response.status_code}")
    print(f"client: {dir(client)}")
    # print(f"client resolve redirect: {client.trace()}")

    # admin_response = client.get('/admin/')
    # print(f"response: {admin_response}, status: {admin_response.status_code}")
    # assert admin_response.status_code == 200
"""

from flask.testing import FlaskClient
def test__register_post(flask_app, load_admin_data, database):
    
    user_data = {
        "username":load_admin_data['email'],
        "password":hash_password(load_admin_data['password'])
        }

    flask_app.test_client_class = FlaskClient
    # flask_app.db = database

    with flask_app.test_request_context():

        with flask_app.test_client() as client:

            print(f"user.register: {url_for('security.register')}")
            print(f"user.login: {url_for('security.login')}")
            print(f"admin: {url_for('admin.index')}")

            register_response = client.post('/user/register', data=user_data, follow_redirects=True)

            print(f"register_response: {register_response}")

            print(f"base request: {request}")
            print(f"base request form: {request.form}")
            print(f"base request cookies: {request.cookies}")

            print(f"base session: {session}")
            
            print(f"base g: {g.__dict__}")
            print(f"check db for users")
            print(f"<Users: {[x for x in User.objects()]}")


            login_response = client.post('/user/sign-in', data=user_data, follow_redirects=True)

            print(f"login_response: {login_response}")
            print(f"2 request: {request}")
            print(f"2 request form: {request.form}")
            # print(f"2 request headers: {request.headers}")
            print(f"2 request cookies: {request.cookies}")

            print(f"2 session: {session}")
            # print(f"2 g: {g.__dict__}")

            admin_response = client.get('/admin/', follow_redirects=True)

            print(f"admin_response: {admin_response}")
            print(f"3 request: {request}")
            print(f"3 request data: {request.data}")
            # print(f"3 request headers: {request.headers}")
            print(f"3 request cookies: {request.cookies}")

            print(f"3 session: {session}")
            # print(f"3 g: {g.__dict__}")
            print(f"app.db: {flask_app.db}")
            print(f"database: {database}")

            assert admin_response.status_code == 200

# def test_user_class_db(database):
#     user = User.objects().first()
#     print(f"user db: {user._get_db()}")

