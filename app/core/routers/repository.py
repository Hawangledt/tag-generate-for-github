import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.models.database import get_db
from core.models.table import RepoDB
from core.routers.auth import _get_user_auth_id
from core.routers.tag import _get_all_tags_in_repo


router = APIRouter(prefix="/repos")


def _request_github_api(user_name):
    url = 'https://api.github.com/users/{user_name}/starred'.format(
        user_name=user_name)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def _get_repos_in_db(db: Session, auth_user_id: str):
    return db.query(RepoDB).filter(
        RepoDB.auth_id == auth_user_id).all()


def _get_repos_in_github(user_name):
    api_data = _request_github_api(user_name)
    list_of_repos = []
    if type(api_data) is not int:
        for repo in range(len(api_data)):
            starred_repo = {
                "github_repo_id":  api_data[repo]['id'],
                "name": api_data[repo]['name'],
                "description": api_data[repo]['description'],
                "html_url": api_data[repo]['html_url']
            }
            list_of_repos.append(starred_repo)
        return list_of_repos
    else:
        return api_data


def _get_repo_by_id(db: Session, github_repo_id: int):
    return db.query(RepoDB).filter(
        RepoDB.github_repo_id == github_repo_id).first()


def _get_repos_info(db: Session, auth_user_id: str):
    repos = _get_repos_in_db(db=db, auth_user_id=auth_user_id)
    list_of_repos = []
    for repo in repos:
        repo_info = {
            "id": repo.id,
            "github_repo_id":  repo.github_repo_id,
            "name": repo.name,
            "description": repo.description,
            "html_url": repo.html_url,
            "tags": _get_all_tags_in_repo(repo_id=repo.id, db=db)
        }
        list_of_repos.append(repo_info)

    return list_of_repos


def _verify_starred_repo(db: Session, user_name: str):
    repos_in_db = _get_repos_in_db(db=db, auth_user_id=_get_user_auth_id())
    repos_in_github = _get_repos_in_github(user_name=user_name)

    for repo in repos_in_db:
        repo.is_starred_repo = False
        db.flush()

    for repo in repos_in_github:
        starred_repo = _get_repo_by_id(db=db,
                                       github_repo_id=repo['github_repo_id'])
        if starred_repo:
            starred_repo.is_starred_repo = True
            starred_repo.name = repo['name']
            starred_repo.description = repo['description']
            starred_repo.html_url = repo['html_url']
            db.flush()
        else:
            db_repo = RepoDB(github_repo_id=repo['github_repo_id'],
                             auth_id=_get_user_auth_id(),
                             is_starred_repo=True,
                             name=repo['name'],
                             description=repo['description'],
                             html_url=repo['html_url'])
            db.add(db_repo)
            db.flush()

    db.commit()
    repos_info = _get_repos_info(db=db, auth_user_id=_get_user_auth_id())

    return repos_info


@router.get(
    "/",
    name="Search Starred Repositories",
    description="""Search the github api for all
    starred repositories for the specified user""",
    responses={
        200: {
        }
    }
)
async def refresh_repos(db: Session = Depends(get_db)):
    repos = _verify_starred_repo(db=db, user_name="Hawangledt")
    return repos
