import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Recipe App"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./recipe_app.db")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "sk-or-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
