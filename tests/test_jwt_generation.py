import jwt
from httpx import AsyncClient

from src.config import settings


async def test_jwt_generation_login_admin(client: AsyncClient) -> None:
    """Лабораторна 8: Отримання JWT токена для admin через POST /api/v1/auth/login."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "admin"
    assert data["role"] == "ADMIN"
    assert data["authorities"] == ["ADMIN"]

    # Перевірка декодування JWT токена (аналог jwt.io)
    payload = jwt.decode(
        data["access_token"],
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["sub"] == "admin"
    assert payload["role"] == "ADMIN"
    assert payload["authorities"] == ["ADMIN"]
    assert "iat" in payload
    assert "exp" in payload


async def test_jwt_generation_authenticate_alias(client: AsyncClient) -> None:
    """Лабораторна 8: Перевірка ендпоінта /auth/authenticate у форматі викладача."""
    response = await client.post(
        "/auth/authenticate",
        json={"email": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token"] == data["access_token"]
    assert data["username"] == "admin"
    assert data["authorities"] == ["ADMIN"]


async def test_jwt_generation_login_user(client: AsyncClient) -> None:
    """Лабораторна 8: Отримання JWT токена для звичайного користувача user."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "user", "password": "user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "USER"
    assert data["authorities"] == ["USER"]

    payload = jwt.decode(
        data["access_token"],
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["sub"] == "user"
    assert payload["role"] == "USER"
    assert payload["authorities"] == ["USER"]


async def test_jwt_generation_invalid_credentials(client: AsyncClient) -> None:
    """Лабораторна 8: Спроба отримання токена з невірним паролем — 401 Unauthorized."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong_password"},
    )
    assert response.status_code == 401
