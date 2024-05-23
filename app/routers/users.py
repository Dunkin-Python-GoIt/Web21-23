from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..databases.db import get_db
from ..repository import auth_repo
from ..schemas import user_schema


router = APIRouter(prefix="/users")


@router.post("/login", response_model=user_schema.Token)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), 
    db: dict = Depends(get_db)):
    username = body.username
    user = auth_repo.get_user(db, username)
    token = user_schema.Token(access_token=auth_repo.create_access_token({"sub": user.username}))
    
    return token