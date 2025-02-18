from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:enterprise@localhost:5432/airfluence_db"
    cors_origins: list = ["http://localhost:3000"]
    jwt_secret: str = "some-secret-key"


settings = Settings()


DATABASE_URL = "postgresql://postgres:enterprise@localhost:5432/airfluence_db"
