from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class AppSettings(BaseSettings):
    DATABASE_URL: str
    APP_SECRET_KEY: str


settings = AppSettings(".env")
