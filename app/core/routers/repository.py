from fastapi import APIRouter
import requests


router = APIRouter(prefix="/repos")


class ListOfStarredRepos():
    """ Initializing the object with a GitHub username returns,
     if you call the get_repos () method,
      a list of all starred repositories
    """

    def __init__(self, user):
        self._user = user

    def __print__(self):
        return self._user

    def request_api(self):
        url = 'https://api.github.com/users/{user_name}/starred'.format(
            user_name=self._user)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code

    def get_repos(self):
        api_data = self.request_api()
        list_of_repos = []
        if type(api_data) is not int:
            for repo in range(len(api_data)):
                starred_repo = {
                    "id":  api_data[repo]['id'],
                    "name": api_data[repo]['name'],
                    "description": api_data[repo]['description'],
                    "html_url": api_data[repo]['html_url']
                }
                list_of_repos.append(starred_repo)
            return list_of_repos
        else:
            return(api_data)


@router.get(
    "/get/{user_name}",
    name="Search Starred Repositories",
    description="""Search the github api for all
    starred repositories for the specified user""",
    responses={
        200: {
        }
    }
    )
async def repos(user_name: str):
    repos = ListOfStarredRepos(user_name)
    return repos.get_repos()
