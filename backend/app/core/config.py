from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Autonomous SaaS Agent"
    environment: str = "local"
    database_url: str = "sqlite:///./agent.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    langsmith_tracing: bool = False
    pinecone_api_key: str | None = None
    pinecone_index: str = "autonomous-saas-agent"
    monthly_budget_usd: float = 100.0

    model_config = SettingsConfigDict(env_file=".env", env_prefix="ASA_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
