from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_repos_success():
    user_name = "Hawangledt"
    response = client.get("/repos/get/{}".format(user_name))
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_repos_failed():
    user_name = "FakeNameForT&est"
    response = client.get("/repos/get/{}".format(user_name))
    assert response.status_code == 200
    assert response.json() == 404
