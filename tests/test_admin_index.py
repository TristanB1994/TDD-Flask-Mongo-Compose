from flask import url_for, request, session
from flask_security import current_user

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