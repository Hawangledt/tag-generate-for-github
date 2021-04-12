import json

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_new_tag_1():
    test_request_payload = {
        'name': "Flask",
        'auth_id': 1
    }
    test_response_payload = {
        'id': "any_integer",
        'name': "Flask",
        'auth_id': 1
    }
    response = client.post("/tags/new", data=json.dumps(test_request_payload))
    assert response.status_code == 200
    response_json = response.json()
    test_response_payload['id'] = response_json['id']
    assert response_json == test_response_payload


def test_create_new_tag_2():
    test_request_payload = {
        'name': "Flask",
        'auth_id': 1
    }
    test_response_payload = {
        "detail": "Tag already registered"
    }
    response = client.post("/tags/new", data=json.dumps(test_request_payload))
    assert response.status_code == 400
    response_json = response.json()
    assert response_json == test_response_payload


def test_get_tag_by_name():
    test_request_payload = {
        'tag_name': "Flask",
        'auth_id': 1
    }
    test_response_payload = {
        'id': "any_integer",
        'name': "Flask",
        'auth_id': 1
    }
    response = client.get("/tags/get_tag/by_name",
                          data=json.dumps(test_request_payload))
    assert response.status_code == 200
    response_json = response.json()
    test_response_payload['id'] = response_json['id']
    assert response_json == test_response_payload
