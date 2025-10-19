from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Ticketing System"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@ticketing.com"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # CORS
    BACKEND_CORS_ORIGINS: str = '["http://localhost:5173","http://localhost:3000"]'
    
    @property
    def cors_origins(self) -> List[str]:
        return json.loads(self.BACKEND_CORS_ORIGINS)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
