""" WIP
    For the authentication system I will use Auth0.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.models.database import get_db
from core.models.table import AuthDB
from core.models.schema import Auth, AuthCreate

router = APIRouter(prefix="/auth")


def _get_user_auth_id():
    """WIP, return a hardcoded auth_id for code develop

    Returns:
        int: auth_id
    """
    return 1


def _get_auth(db: Session, auth0_unique_id: int):
    return db.query(AuthDB).filter(
        AuthDB.auth0_unique_id == auth0_unique_id).first()


def _create_auth(db: Session, auth: AuthCreate):
    db_auth = AuthDB(auth0_unique_id=auth.auth0_unique_id,
                     github_nickname=auth.github_nickname)
    db.add(db_auth)
    db.commit()
    db.refresh(db_auth)
    return db_auth


def _delete_auth():
    pass


@router.get("/new/",
            name="Create a new user",
            description="""Binds the user with auth0 registration
             in the system""",
            response_model=Auth)
def create_auth(auth: AuthCreate, db: Session = Depends(get_db)):
    db_auth = _get_auth(db, auth0_unique_id=auth.auth0_unique_id)
    if db_auth:
        raise HTTPException(
            status_code=400, detail="auth_unique_id already registered")
    return _create_auth(db=db, auth=auth)
