from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings and environment configuration.
    Expert implementation: Centralized, validated, and type-safe.
    """
    PROJECT_NAME: str = "voter.ai"
    API_V1_STR: str = "/api/v1"
    
    # GCP Config
    GCP_PROJECT_ID: str = "promptwars-c2"
    GCP_LOCATION: str = "us-central1"
    GCS_BUCKET_NAME: str = "voter-ai-logs-promptwars-c2"
    
    # Security
    ALLOWED_ORIGINS: list[str] = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 60
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

@lru_cache()
def get_settings():
    """
    Returns a cached instance of the settings.
    """
    return Settings()

settings = get_settings()
