from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Car systems"
    secrets_key: str
    mail_password: str
    url:str
    
    class Config:
        env_file = ".env"
        env_prefix="api_"


settings = Settings()
        