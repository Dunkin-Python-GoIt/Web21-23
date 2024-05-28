from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    username: str


class User(BaseUser):
    hashed_password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")