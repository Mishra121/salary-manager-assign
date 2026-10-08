"""Application configuration and settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # App
    app_name: str = "Salary Management System"
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: str = "sqlite:///./salary_management.db"
    database_echo: bool = False

    # API
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
