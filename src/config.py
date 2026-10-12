from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Web Security Labs API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    # Налаштування безпеки за замовчуванням (аналог spring.security.user.* у Spring Security)
    security_user_name: str = "admin"
    security_user_password: str = "admin"
    jwt_secret_key: str = "super-secret-web-sec-labs-key-2026"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


settings = Settings()
