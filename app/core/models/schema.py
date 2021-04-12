from pydantic import BaseModel


class AuthSchema(BaseModel):
    auth0_unique_id: str
    github_nickname: str


class AuthCreate(AuthSchema):
    pass


class Auth(AuthSchema):
    id: int
    auth0_unique_id: str
    github_nickname: str

    class Config:
        orm_mode = True


class TagSchema(BaseModel):
    name: str
    auth_id: int


class TagCreate(TagSchema):
    pass


class Tag(TagSchema):
    id: int
    name: str
    auth_id: int

    class Config:
        orm_mode = True


class RepoSchema(BaseModel):
    github_repo_id: int
    auth_id: int
    is_starred_repo: bool
    name: str
    description: str
    html_url: str


class RepoCreate(TagSchema):
    pass


class Repo(TagSchema):
    id: int
    github_repo_id: int
    auth_id: int
    is_starred_repo: bool
    name: str
    description: str
    html_url: str

    class Config:
        orm_mode = True


class TagInRepoSchema(BaseModel):
    tag_id: int
    repo_id: int


class TagInRepoCreate(TagInRepoSchema):
    pass


class TagInRepo(TagInRepoSchema):
    id: int
    tag_id = int
    repo_id = int

    class Config:
        orm_mode = True
