from datetime import datetime, timezone, timedelta
from typing import Optional, Annotated

from passlib.context import CryptContext
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..schemas import user_schema
from ..databases.db import get_db


SECRET_KEY = "secret_key"
ALGORITHM = "HS256"


class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"])

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, plain_password: str):
        return self.pwd_context.hash(plain_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def get_user(db: dict, username: str):
    users = [user for user in db["users"] if user["username"] == username]
    if users:
        user = user_schema.User(**users[0])
        return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user = get_user(get_db(), username)
    return user


def create_access_token(data: dict, expires_delta: Optional[float] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire, "scope": "access_token"})
    encoded_access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_access_token


class RoleChecker:
    def __init__(self, allowed_role):
        self.allowed_role = allowed_role
    
    def __call__(self, user: Annotated[user_schema.User, Depends(get_current_user)]):
        if user.role == self.allowed_role:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
