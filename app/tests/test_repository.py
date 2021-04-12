from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUser:
    def create_user():
        fake_user = {
            auth0_unique_id: "fake_auth0_id"
            github_nickname: "fake_github_nickname"
        }
        response = client.get("/auth/new/",
                              data=json.dumps(test_fake_auth))
        return auth0_unique_id

    def remove_user():
        pass


fake_user = TestUser()


def test_api_gituhub_get_repos_success():
    user_name = "Hawangledt"
    response = client.get("/repos/get/{}".format(user_name))
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_api_gituhub_get_repos_failed():
    user_name = "FakeNameForT&est"
    response = client.get("/repos/get/{}".format(user_name))
    assert response.status_code == 200
    assert response.json() == 404


# adicionar um repositório com estrela no banco de dados
def test_add_starred_repos_in_db():
    # add a fake user
    fake_auth0_unique_id = fake_user.create_user()
    # add a fake repo
    test_request_payload = [
        {
            "id": 'any_integer',
            "github_repo_id": 101,
            "auth_id": fake_auth0_unique_id,
            "is_starred_repo": True,
        },
    ]
    test_response_payload = [
        {
            "id": 'any_integer',
            "github_repo_id": 101,
            "auth_id": fake_auth0_unique_id,
            "is_starred_repo": True,
        },
    ]

    url = "/repos/{fake_auth0_unique_id}/add/".format(test_request_payload)
    response = client.post(url,
                           data=json.dumps(test_fake_repo))
    assert response.status_code == 200
    response_json = response.json()
    test_response_payload['id'] = response_json['id']
    assert response_json == test_response_payload
    # delete a fake repo
    # delete a fake user
    fake_user.remove_user()

# adicionar os repositórios com estrela no banco de dados
    # add a fake user
    # add a fake repos list
    # delete a fake repos list
    # delete a fake user

    # verificar se os repositórios no bd ainda estão marcados com star
    # se não estiver marked with star,
    #        change state (is_starred_repo) to [False]

    # adicionar uma tag a um repositorio
    # não deixar adicionar a mesma tag a um repositório

    # remover uma tag de um repositorio
    # não remover uma tag que não esta associada ao repositório

    # Pesquisar os repositórios passando o nome de uma tag
