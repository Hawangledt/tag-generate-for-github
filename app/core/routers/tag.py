from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.models.table import TagDB, TagInRepoDB
from core.models.schema import Tag, TagCreate, TagSchema
from core.models.schema import TagInRepo, TagInRepoCreate, TagInRepoSchema
from core.models.database import get_db
from core.routers.auth import _get_user_auth_id

router = APIRouter(prefix="/tags")


def _create_tag(db: Session, tag: TagCreate):
    db_tag = TagDB(name=tag.name, auth_id=tag.auth_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def _get_tag_by_name(tag_name: str, auth_id: int, db: Session):
    return db.query(TagDB).filter(TagDB.name == tag_name,
                                  TagDB.auth_id == auth_id).first()


def _get_tag_by_id(tag_id: int, db: Session):
    return db.query(TagDB).filter(TagDB.id == tag_id).first()


def _get_all_tags(db: Session, auth_id: int):
    return db.query(TagDB).filter(auth_id == auth_id).all()


def _add_tag_in_repo(tag_in_repo: TagInRepoCreate, db: Session):
    db_tag_in_repo = TagInRepoDB(repo_id=tag_in_repo.repo_id,
                                 tag_id=tag_in_repo.tag_id)
    db.add(db_tag_in_repo)
    db.commit()
    db.refresh(db_tag_in_repo)
    return db_tag_in_repo


def _get_tag_in_repo(repo_id: int, tag_id: int, db: Session):
    return db.query(TagInRepoDB).filter(TagInRepoDB.repo_id == repo_id,
                                        TagInRepoDB.tag_id == tag_id).first()


def _get_all_tags_in_repo(repo_id: int, db: Session):
    tags_in_repo = db.query(TagInRepoDB).filter(
        TagInRepoDB.repo_id == repo_id).all()
    tags = []
    for tag in tags_in_repo:
        tag_data = _get_tag_by_id(
            tag_id=tag.tag_id, db=db)
        tag_info = {
            "id": tag_data.id,
            "name": tag_data.name
        }
        tags.append(tag_info)
    return tags


def _remove_tag_in_repo(tag_in_repo_id: int, db: Session):
    db_tag_in_repo = db.query(TagInRepoDB).filter(
        TagInRepoDB.id == tag_in_repo_id).first()
    db.delete(db_tag_in_repo)
    db.commit()


@router.post("/new",
             name="Create a new tag",
             description="""Checks that there is no tag
              with the same name and then adds it to the system""",
             response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = _get_tag_by_name(db=db, tag_name=tag.name, auth_id=tag.auth_id)
    if db_tag:
        raise HTTPException(
            status_code=400, detail="Tag already registered")
    return _create_tag(db=db, tag=tag)


@router.get("/all/",
            name="Get all user tags",
            description="""Finds all tags linked to the user""",
            responses={
                200: {
                }
            })
def get_all_tags(db: Session = Depends(get_db)):
    auth_id = _get_user_auth_id()
    db_tag = _get_all_tags(db=db, auth_id=auth_id)
    return db_tag


@router.post("/add",
             name="Adds a tag to a repository",
             description="""Associates a tag in a repository""",
             response_model=TagInRepo)
def add_tag_in_repo(tag_in_repo: TagInRepoCreate,
                    db: Session = Depends(get_db)):
    db_tag_in_repo = _get_tag_in_repo(repo_id=tag_in_repo.repo_id,
                                      tag_id=tag_in_repo.tag_id,
                                      db=db)
    if db_tag_in_repo:
        raise HTTPException(
            status_code=400, detail="Tag is already associated")
    return _add_tag_in_repo(tag_in_repo=tag_in_repo,
                            db=db)


@router.delete("/{repo_id}/{tag_id}",
               name="Removes a tag from a repository",
               description="""Deletes a tag associated with a repository""",
               response_model=TagInRepo)
def remove_tag_in_repo(repo_id: int,
                       tag_id: int,
                       db: Session = Depends(get_db)):
    db_tag_in_repo = _get_tag_in_repo(repo_id=repo_id,
                                      tag_id=tag_id,
                                      db=db)
    if not db_tag_in_repo:
        raise HTTPException(
            status_code=404, detail="Tag not is associated")

    _remove_tag_in_repo(tag_in_repo_id=db_tag_in_repo.id, db=db)
    return db_tag_in_repo
