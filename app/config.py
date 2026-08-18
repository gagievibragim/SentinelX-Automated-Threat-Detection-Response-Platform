from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./sentinelx.db"
    redis_url: str = "redis://localhost:6379/0"
    rules_path: str = "app/detection/rules"
    risk_threshold: int = 50

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
