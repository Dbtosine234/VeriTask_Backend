import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "VeriTask API")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))


settings = Settings()
