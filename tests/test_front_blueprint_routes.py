from application.front_blueprint import front_blueprint
from flask import Flask
import pytest

def test__front_blueprint_route_rules(bp_routes):
    rules = bp_routes(front_blueprint)
    print(f"rules: {rules}")

    routes = [ x.rule for x in rules ]
    # print(f"routes: {routes}")

    assert routes == ['/users', '/']


def test__front_blueprint_index_get(client):
    response = client.get('/')
    # print(f"response data: {response.data}")
    # print(f"response status_code: {response.status_code}")
    assert response.status_code == 200

def test__front_blueprint_users_get(client):
    response = client.get('/users')
    assert response.status_code == 200