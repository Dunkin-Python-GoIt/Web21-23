from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from ..databases.db import get_db
from ..repository import auth_repo
from ..schemas import user_schema


router = APIRouter(prefix="/users")

receivers = [
            "oleg.davidenko@gmail.com",
            "dnepr.life@gmail.com",
            "v.dunkin@goit.ua", 
            "artem_madrid@hotmail.com",
            "tapxyh1445@gmail.com",
            "kadulin@gmail.com"
            ]

conf = ConnectionConfig(
    MAIL_USERNAME ="<your mail>",
    MAIL_PASSWORD = "<your password>",
    MAIL_FROM = "<your mail>",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@router.post("/login", response_model=user_schema.Token)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), 
    db: dict = Depends(get_db)):
    username = body.username
    pwd = body.password
    user = auth_repo.authenticate_user(db, username, pwd)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password")
    token = user_schema.Token(access_token=auth_repo.create_access_token({"sub": user.username}))
    return token


@router.post("/forget_password")
async def forget_password(
    background_tasks: BackgroundTasks,
    user: user_schema.BaseUser,
    db: dict = Depends(get_db)
):
    user = auth_repo.get_user(db, user.username)
    new_token = auth_repo.create_access_token({"username": user.username})
    
    
    if user:
        forget_password_link = f"http://127.0.0.1:8000/api/users/reset_password/{new_token}"
    
    mail_body = {
        "service_name": "My site",
        "reset_link": forget_password_link
    }
    
    message = MessageSchema(
        subject="Reset password",
        recipients=receivers,
        template_body=forget_password_link,
        subtype=MessageType.plain
    )
    
    email_service = FastMail(conf)
    
    background_tasks.add_task(email_service.send_message, message)
    
    return forget_password_link


@router.post("/reset_password/{token:str}")
async def reset_password():
    ...