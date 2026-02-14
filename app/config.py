from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    APP_NAME: str = "AI Doctor Assistant API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./doctor_assistant.db"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OTP_EXPIRY_MINUTES: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
