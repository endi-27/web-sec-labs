from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Web Security Labs API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    # Налаштування підключення до PostgreSQL
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "websec_user"
    db_password: str = "websec_password"
    db_name: str = "websec_db"

    # Налаштування JWT
    jwt_secret_key: str = "super-secret-web-sec-labs-key-2026"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
