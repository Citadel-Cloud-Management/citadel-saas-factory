from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    project_name: str = "citadel-saas-factory"
    env: str = "development"
    database_url: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    jwt_secret: str
    rate_limit_per_minute: int = 120
    cors_origins: str = "http://localhost:3000"


settings = Settings()
